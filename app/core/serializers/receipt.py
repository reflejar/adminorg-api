from datetime import date, timedelta

from django.db.models import Max
from rest_framework import serializers

from django_afip.models import (
	ConceptType,
	PointOfSales,
	Receipt,
	ReceiptType,
	CurrencyType
)
from utils.models import Comunidad
from core.models import OwnReceipt 

class ReceiptModelSerializer(serializers.ModelSerializer):
	'''Receipt model serializer'''
	# currency = serializers.SerializerMethodField()

	class Meta:
		model = OwnReceipt

		fields = (
			'issued_date',
			'currency_quote',
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['total_amount'] = serializers.DecimalField(
				max_digits=15, 
				decimal_places=2, 
				read_only=True
			)

		self.fields['receipt_type'] = serializers.ChoiceField(
			choices=list(ReceiptType.objects.all().values_list('description', flat=True)),
			label="Tipo"
		)
		self.fields['currency'] = serializers.ChoiceField(
			choices=list(CurrencyType.objects.all().values_list('code', flat=True)),
			label="Moneda"
		)		
		point_of_sales_owner = list(PointOfSales.objects.filter(owner=self.context['comunidad'].contribuyente).values_list('number', flat=True))
		if self.context['causante'] in ["cliente", "caja"]:
			self.fields['point_of_sales'] = serializers.ChoiceField(
				choices=point_of_sales_owner, 
				label="Punto de venta"
			)
			self.fields['receipt_number'] = serializers.IntegerField(
				read_only=True,
				label="Número"
			)
			
		elif self.context['causante'] == "proveedor":
			if 'receipt_type' in self.context.keys():
				self.fields['point_of_sales'] = serializers.CharField(
					max_length=4, 
					required=True,
					label="Punto de venta"
				)
				if self.context['receipt_type'].code != "301":
					self.fields['receipt_number'] = serializers.IntegerField(
						read_only=False, 
						required=True,
						label="Número"
					)
				else:
					self.fields['receipt_number'] = serializers.IntegerField(
						read_only=True,
						label="Número"
					)
			else:
				self.fields['point_of_sales'] = serializers.CharField(
					read_only=True,
					label="Punto de venta"
				)
				self.fields['receipt_number'] = serializers.IntegerField(
					read_only=True,
					label="Número"
				)
				
		elif self.context['causante'] == "asiento":
			self.fields['receipt_number'] = serializers.IntegerField(
				read_only=True,
				label="Número"
			)

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['currency'] = instance.currency.code  # Obtiene el código de la moneda
		return representation



	def get_point_of_sales(self, point_of_sales):

		return PointOfSales.objects.get(owner=self.context['comunidad'].contribuyente, number=point_of_sales)

	def validate_currency(self, currency):
		"""
			Para convertir el currency en objeto CurrencyType
		"""
		return CurrencyType.objects.get(code=currency)	

	def validate_concept(self, concept):
		"""
			Para convertir el concept en objeto ConceptType
		"""
	
		return ConceptType.objects.get(description=concept)	


	def create(self, validate_data):
		afip = validate_data.pop('afip') 

		receipt = OwnReceipt.objects.create(**validate_data)

		receipt_afip = None
		if afip:
			validate_data['point_of_sales'] = self.get_point_of_sales(validate_data['point_of_sales'])
			receipt_afip = Receipt.objects.create(**validate_data)
			try:
				error = receipt_afip.validate()
			except Exception as e:
				print(e)
				raise serializers.ValidationError({'afip_error':'No se pudo validar en AFIP. Vuelve a intentarlo mas tarde'})			

		receipt.save()
		return receipt, receipt_afip