from datetime import timedelta

from django.db import transaction

from rest_framework import serializers
from datetime import date

from apps.core.models import (
	Documento,
	Cuenta, 
)
from django_afip.models import (
	ConceptType,
	CurrencyType
)
from apps.core.serializers import ReceiptModelSerializer

from .operaciones.carga import CargaModelSerializer
from .operaciones.cobro import CobroModelSerializer
from .operaciones.caja import CajaModelSerializer
from .operaciones.resultado import ResultadoModelSerializer

from apps.core.CU.comprobante import CU


class ComprobanteModelSerializer(serializers.ModelSerializer):
	'''Documento model serializer'''
	pdf = serializers.SerializerMethodField()
	
	class Meta:
		model = Documento

		fields = (
			'id',
			'descripcion',
			'fecha_anulacion',
			'nombre',
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
			self.fields['cajas'] = CajaModelSerializer(context=self.context, read_only=False, many=True)
			self.fields['resultados'] = ResultadoModelSerializer(context=self.context, read_only=False, many=True)
			

	def validate_fecha_operacion(self, fecha_operacion):

		"""
			Validacion de fecha_operacio
			Hoy en dia se puede cualquier fecha.
			Habria que agregar que no se pueden hacer con fecha anterior a un periodo cerrado
		"""
		
		return fecha_operacion			

	def get_pdf(self, instance):
		return None
		request = self.context['request']
		if instance.pdf:
			pdf_url = instance.pdf.serve().url
			return request.build_absolute_uri(pdf_url)
		return None
	
	def valid_cobros(self, data):
		"""
			Validacion de cobros.
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de las cargas juntos
			No se permite si:
				la carga no pertenece a al destinatario
				existe un pago de capital posterior a la fecha_operacion recibida
				el "valor" colocado para la carga es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario_documento = data['destinatario']
		fecha_operacion = data['fecha_operacion']
		cobros = data['cobros']
		for d in cobros:
			carga = d['vinculo']
			if carga.cuenta != destinatario_documento:
				raise serializers.ValidationError({'cobros': {carga.id: "No es una carga perteneciente al cliente"}})

			pagos = carga.pagos_capital()
			if pagos:
				if pagos.filter(fecha__gt=fecha_operacion, documento__fecha_anulacion__isnull=True):
					raise serializers.ValidationError({'cobros': {carga.id: "La carga que desea abonar posee un pago de capital posterior"}})

			if carga.saldo(fecha=fecha_operacion) < d['monto']:
				raise serializers.ValidationError({'cobros': {carga.id: "El valor colocado es mayor al saldo de la carga que desea abonar"}})


	def valid_totales(self, data):
		"""
			Validacion de total en recibos.
			No se permite si:
				la suma de los cobros es mayor a la suma de las cajas y las utilizaciones_saldos
		"""
		suma = 0
		suma_cobros = sum([i['monto'] for i in data['cobros']])
		suma_cajas = sum([i['monto'] for i in data['cajas']])
		suma_resultados = sum([i['monto'] for i in data['resultados']])

		if suma_cobros > suma_cajas + suma_resultados:
			raise serializers.ValidationError('El valor de las cargas que intenta cobrar es mayor al total por formas de cobro')

		return suma


	def validate(self, data):
		"""
			Validacion de issued_date. 
			Solo se puede hacer en la validacion grupal para poder acceder a point_of_sales e issued_date juntos
			No se permite si
				Ya tiene un documento con fecha anterior a la solicitada
				10 dias anterior o posterior a la fecha actual
		"""

		if self.context['causante'] in ["cliente"]:
			point_of_sales = data["receipt"]["point_of_sales"]
			issued_date = data["receipt"]["issued_date"]
			receipt_type = self.context['receipt_type']
			query = Documento.objects.filter(
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

		return data

	def hacer_total(self, validated_data):
		"""Crea el total_amount"""

		total = sum([i['monto'] for i in validated_data['cajas']]) \
			 or sum([i['monto'] for i in validated_data['resultados']]) \
		     or sum([i['monto'] for i in validated_data['cargas']]) \
			 or 0.00
		
		return total
		
	@transaction.atomic		
	def create(self, validated_data):
		destinatario = validated_data['destinatario'] or None
		document_type = None
		document_number = None
		if destinatario:
			if destinatario.perfil:
				document_type = destinatario.perfil.tipo_documento
				document_number = destinatario.perfil.numero_documento

		fecha_operacion = validated_data['fecha_operacion']
		descripcion = validated_data['descripcion']

		# Receipt
		receipt_data = validated_data['receipt']
		validated_data['receipt']['total_amount'] = self.hacer_total(validated_data)
		receipt_data.update({
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
		
		# if self.context['comunidad'].contribuyente.certificate: # Si la comunidad tiene un certificado en el contribuyente de afip
		# 	if destinatario: # Si el documento tiene destinatario
		# 		if destinatario.naturaleza.nombre == "cliente" and self.context['receipt_type'].code in ['11', '12', '13']:
		# 			receipt_data['afip'] = True
				
		


		documento = Documento.objects.create(
			comunidad=self.context['comunidad'],
			receipt=receipt,
			receipt_afip=receipt_afip,
			destinatario=destinatario,
			fecha_operacion=fecha_operacion,
			descripcion=descripcion,
		)		
		documento.chequear_numeros()

		
		CU(documento, validated_data).create()
		documento.hacer_pdf()

		# # self.send_email(documento)
		return documento

	# def send_email(self, documento):
	# 	if documento.pdf:
	# 		attachments = Attachment.objects.create(pdf=documento.pdf)
	# 		q = Queue.objects.create(
	# 			comunidad=documento.comunidad,
	# 			addressee=documento.destinatario.perfil,
	# 			subject="Nuevo Comprobante",
	# 			body=render_to_string('emails/documentos/index.html', {"documento": documento}),
	# 			client="core.serializers.documentos.cliente.DestinoClienteModelSerializer",
	# 			execute_at=datetime.now()
	# 		)
	# 		q.attachments.add(attachments)
