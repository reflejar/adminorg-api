from datetime import date, timedelta

from django.db.models import Max
from rest_framework import serializers

from admincu.utils.models import Comunidad
from django_afip.models import (
	ConceptType,
	PointOfSales,
	Receipt,
	ReceiptType
)


class ReceiptModelSerializer(serializers.ModelSerializer):
	'''Receipt model serializer'''

	class Meta:
		model = Receipt

		fields = (
			'issued_date',
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['total_amount'] = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
		self.fields['receipt_type'] = serializers.ChoiceField(choices=list(ReceiptType.objects.all().values_list('description', flat=True)))
		point_of_sales_owner = list(PointOfSales.objects.filter(owner=self.context['comunidad'].contribuyente).values_list('number', flat=True))
		
		if self.context['causante'] in ["cliente", "caja"]:
			self.fields['point_of_sales'] = serializers.ChoiceField(choices=point_of_sales_owner)
			self.fields['receipt_number'] = serializers.IntegerField(read_only=True)
			
		elif self.context['causante'] == "cliente-masivo":
			self.fields['point_of_sales'] = serializers.ChoiceField(choices=point_of_sales_owner)
	
		elif self.context['causante'] == "proveedor":
			if 'receipt_type' in self.context.keys():
				self.fields['point_of_sales'] = serializers.CharField(max_length=4, required=True)
				if self.context['receipt_type'].code != "301":
					self.fields['receipt_number'] = serializers.IntegerField(read_only=False, required=True)
				else:
					self.fields['receipt_number'] = serializers.IntegerField(read_only=True)
			else:
				self.fields['point_of_sales'] = serializers.CharField(read_only=True)
				self.fields['receipt_number'] = serializers.IntegerField(read_only=True)


		elif self.context['causante'] == "estado":
			self.fields['formatted_number'] = serializers.CharField(max_length=150, read_only=True)

		elif self.context['causante'] == "asiento":
			self.fields['point_of_sales'] = serializers.CharField(max_length=4, required=True)
			self.fields['receipt_number'] = serializers.IntegerField(read_only=True)


	def validate_point_of_sales(self, point_of_sales):
		"""
			Si el causante es un cliente entonces solo puede elegir uno de los puntos que tiene
			Convierte el numero en objeto
		"""
		if self.context['causante'] in ["cliente", "cliente-masivo"] or self.context['receipt_type'].code in ["301", "303"]:
			point_of_sales = PointOfSales.objects.get(owner=self.context['comunidad'].contribuyente, number=point_of_sales)
		elif self.context['causante'] == "proveedor":
			point_of_sales = PointOfSales.objects.get(owner__name="Proveedores", number=point_of_sales)
		elif self.context['causante'] == "asiento":
			point_of_sales = PointOfSales.objects.get(owner__name="Asientos", number=point_of_sales)
		return point_of_sales

	def validate_concept(self, concept):
		"""
			Para convertir el concept en objeto ConceptType
		"""
	
		return ConceptType.objects.get(description=concept)	


	def validate(self, data):
		"""
			Validacion de issued_date. 
			Solo se puede hacer en la validacion grupal para poder acceder a point_of_sales e issued_date juntos
			No se permite si
				Ya tiene un documento con fecha anterior a la solicitada
				10 dias anterior o posterior a la fecha actual
		"""

		point_of_sales = data["point_of_sales"]
		issued_date = data["issued_date"]
		receipt_type = self.context['receipt_type']

		if self.context['causante'] in ["cliente", "cliente-masivo", "asiento"] or self.context['receipt_type'].code in ["301", "303"]:
			query = point_of_sales.receipts.filter(issued_date__gt=issued_date, receipt_type=receipt_type)
			if query:
				raise serializers.ValidationError({'issued_date': 'El punto de venta seleccionado ha generado {} con fecha posterior a la indicada'.format(receipt_type)})
			if self.context['causante'] == "cliente":
				if date.today() + timedelta(days=10) < issued_date or issued_date < date.today() - timedelta(days=10):
					raise serializers.ValidationError({'issued_date': 'No puede diferir en mas de 10 dias de la fecha de hoy'})

		return data


	def create(self, validate_data):
		afip = validate_data.pop('afip') if 'afip' in validate_data.keys() else False  

		receipt = Receipt.objects.create(**validate_data)

		# if afip:
		# 	try:
		# 		error = receipt.validate()
		# 	except:
		# 		error = True
		# 	if error:
		# 		raise serializers.ValidationError('No se pudo validar en AFIP. Vuelve a intentarlo mas tarde')			

		if not receipt.receipt_number:
			last = Receipt.objects.filter(
				receipt_type=receipt.receipt_type,
				point_of_sales=receipt.point_of_sales,
			).aggregate(Max('receipt_number'))['receipt_number__max'] or 0
			receipt.receipt_number = last + 1
			receipt.save()

		return receipt