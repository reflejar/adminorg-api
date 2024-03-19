from datetime import timedelta

from django.db import transaction

from rest_framework import serializers
from datetime import date

from core.models import (
	Comprobante,
	Cuenta, 
)
from django_afip.models import (
	ConceptType,
	CurrencyType
)
from core.serializers import ReceiptModelSerializer


from .operaciones.carga import CargaModelSerializer
from .operaciones.cobro import CobroModelSerializer
from .operaciones.descarga import DescargaModelSerializer

from core.CU.comprobante import CU


class ComprobanteModelSerializer(serializers.ModelSerializer):
	'''Comprobante model serializer'''
	afip = serializers.SerializerMethodField()
	modulo = serializers.SerializerMethodField()
	pdf = serializers.SerializerMethodField()
	
	class Meta:
		model = Comprobante

		fields = (
			'id',
			'afip',	
			'modulo',
			'descripcion',
			'fecha_anulacion',
			'nombre',
			'link',
			'pdf'
		)
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['fecha_operacion'] = serializers.DateField(initial=date.today())		
		if self.context.keys():
			self.fields['destinatario'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre=self.context['causante']
						), 
					allow_null=True
				)
			self.fields['receipt'] = ReceiptModelSerializer(context=self.context, read_only=False, many=False)
			
			if 'receipt_type' in self.context.keys():
				self.fields['fecha_anulacion'] = serializers.DateField(read_only=True)
				
			self.fields['cargas'] = CargaModelSerializer(context=self.context, read_only=False, many=True)
			self.fields['cobros'] = CobroModelSerializer(context=self.context, read_only=False, many=True, instance=self.instance)
			self.fields['descargas'] = DescargaModelSerializer(context=self.context, read_only=False, many=True)
			
	def get_afip(self, instance): 
		return instance.receipt_afip is not None

	def get_modulo(self, instance): 
		if instance.destinatario:
			return instance.destinatario.naturaleza.nombre
		return ''

	def get_pdf(self, instance):
		return instance.pdf != None
	
	def valid_cobros(self, data):
		"""
			Validacion de cobros.
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de las cargas juntos
			No se permite si:
				la carga no pertenece a al destinatario
				existe un pago de capital posterior a la fecha_operacion recibida
				el "valor" colocado para la carga es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario_comprobante = data['destinatario']
		fecha_operacion = data['fecha_operacion']
		cobros = data['cobros']
		for d in cobros:
			carga = d['vinculo']
			if carga.cuenta != destinatario_comprobante:
				raise serializers.ValidationError({'cobros': {carga.id: "No es una carga perteneciente al cliente"}})

			pagos = carga.pagos_capital()
			if pagos:
				if pagos.filter(fecha__gt=fecha_operacion, comprobante__fecha_anulacion__isnull=True):
					raise serializers.ValidationError({'cobros': {carga.id: "La carga que desea abonar posee un pago de capital posterior"}})

			if carga.saldo(fecha=fecha_operacion) < d['monto']:
				raise serializers.ValidationError({'cobros': {carga.id: "El valor colocado es mayor al saldo de la carga que desea abonar"}})


	def valid_totales(self, data):
		"""
			Validacion de total en recibos.
			No se permite si:
				la suma de los cobros es mayor a la suma de las descargas y las utilizaciones_saldos
		"""
		suma = 0
		suma_cobros = sum([i['monto'] for i in data['cobros']])
		suma_descargas = sum([i['monto'] for i in data['descargas']])

		if suma_cobros > suma_descargas:
			raise serializers.ValidationError('El valor de las cargas que intenta cobrar es mayor al total por formas de cobro')

		return suma

	def valid_update_or_delete(self):
		for c in self.instance.cargas():
			if c.vinculos.all():
				cobrado_en = [str(v.comprobante) for v in c.vinculos.all()]
				raise serializers.ValidationError(f'Primero debe anular o modificar el/los cobro/s realizado/s en {", ".join(cobrado_en)}')

	def validate(self, data):
		"""
			Validacion de issued_date. 
			Solo se puede hacer en la validacion grupal para poder acceder a point_of_sales e issued_date juntos
			No se permite si
				Ya tiene un comprobante con fecha anterior a la solicitada
				10 dias anterior o posterior a la fecha actual
		"""

		if self.context['causante'] in ["cliente"]:
			point_of_sales = data["receipt"]["point_of_sales"]
			issued_date = data["receipt"]["issued_date"]
			receipt_type = self.context['receipt_type']
			query = Comprobante.objects.filter(
				comunidad=self.context['comunidad'],
				receipt__point_of_sales=point_of_sales,
				receipt__receipt_type=receipt_type,
				receipt__issued_date__gt=issued_date,
			)
			if query:
				raise serializers.ValidationError({'issued_date': 'El punto de venta seleccionado ha generado {} con fecha posterior a la indicada'.format(receipt_type)})
			if receipt_type.code in ["11","12","13"]:
				if date.today() + timedelta(days=10) < issued_date or issued_date < date.today() - timedelta(days=10):
					raise serializers.ValidationError({'issued_date': 'No puede diferir en mas de 10 dias de la fecha de hoy'})
		
		self.valid_cobros(data)
		self.valid_totales(data)
		if self.instance:
			self.valid_update_or_delete()

		return data

	def hacer_total(self, validated_data):
		"""Crea el total_amount"""

		total = sum([i['monto'] for i in validated_data['descargas']]) \
		     or sum([i['monto'] for i in validated_data['cargas']]) \
			 or 0.00
		
		return total
		
	@transaction.atomic		
	def create(self, validated_data):
		destinatario = validated_data['destinatario'] or None
		document_type = None
		document_number = None
		afip = False
		if destinatario:
			if self.context['comunidad'].contribuyente.certificate and \
			destinatario.naturaleza.nombre == "cliente" and \
			self.context['receipt_type'].description[-1] == "C":
				afip = True
			if destinatario.perfil:
				document_type = destinatario.perfil.tipo_documento
				document_number = destinatario.perfil.numero_documento

		fecha_operacion = validated_data['fecha_operacion']
		descripcion = validated_data['descripcion']
		link = validated_data['link']

		# Receipt
		receipt_data = validated_data['receipt']
		validated_data['receipt']['total_amount'] = self.hacer_total(validated_data)
		receipt_data.update({
			'afip': afip,
			'receipt_type': self.context['receipt_type'],
			'document_type': document_type,
			'document_number': document_number,

			'total_amount': receipt_data['total_amount'],
			'net_untaxed': 0.00,
			'net_taxed': receipt_data['total_amount'],
			'exempt_amount': 0.00,

			'service_start': receipt_data['issued_date'],
			'service_end': receipt_data['issued_date'],
			'expiration_date': receipt_data['issued_date'],
			'currency': CurrencyType.objects.get(code="PES"),
			'concept': ConceptType.objects.get(description="Productos y servicios")
		})

		receipt, receipt_afip = self.fields['receipt'].create(receipt_data)
		
		comprobante = Comprobante.objects.create(
			comunidad=self.context['comunidad'],
			receipt=receipt,
			receipt_afip=receipt_afip,
			destinatario=destinatario,
			fecha_operacion=fecha_operacion,
			descripcion=descripcion,
			link=link
		)		
		comprobante.chequear_numeros()

		
		CU(comprobante, validated_data).create()
		comprobante.hacer_pdf()

		# # self.send_email(comprobante)
		return comprobante
	

	def update(self, instance, validated_data):
		if instance.receipt_afip: return instance
		# instance.receipt.update(
		# 	point_of_sales=validated_data['receipt']['point_of_sales'],
		# 	issued_date=validated_data['receipt']['issued_date']
		# )
		comprobante = Comprobante.objects.filter(pk=instance.pk)
		comprobante.update(
			fecha_operacion=validated_data['fecha_operacion'],
			descripcion=validated_data['descripcion'],		
			link=validated_data['link'],		
		)

		instance = comprobante.first()
		instance.operaciones.all().delete()
		
		CU(instance, validated_data).create()
		instance.hacer_pdf()


		return instance