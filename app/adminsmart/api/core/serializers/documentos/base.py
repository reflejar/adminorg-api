from rest_framework import serializers

from django_afip.models import (
	Receipt,
	ReceiptType,
	PointOfSales,
	ConceptType,
	DocumentType,
	CurrencyType
)

from adminsmart.apps.core.models import (
	Documento,
	Cuenta, 
	OwnReceipt
)
from adminsmart.api.core.serializers import ReceiptModelSerializer



class DocumentoModelSerializer(serializers.ModelSerializer):
	'''Documento model serializer'''
	pdf = serializers.SerializerMethodField()
	
	class Meta:
		model = Documento

		fields = (
			'id',
			'fecha_operacion',
			'descripcion',
			'fecha_anulacion',
			'nombre',
			'pdf'
		)
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Fields comunes:
		# self.fields['pdf'] = serializers.FileField(read_only=True)
		if self.context.keys():
			if not self.context['sin_destinatario']:
				self.fields['destinatario'] = serializers.PrimaryKeyRelatedField(
						queryset=Cuenta.objects.filter(
								comunidad=self.context['comunidad'], 
								naturaleza__nombre=self.context['causante']
							), 
						allow_null=False
					)
				self.fields['portador'] = serializers.CharField(max_length=200, read_only=True)		
			self.fields['receipt'] = ReceiptModelSerializer(context=self.context, read_only=False, many=False)
			
			if 'receipt_type' in self.context.keys():
				if self.context['receipt_type'].code in ["54", "301", "303"]:
					self.fields['fecha_anulacion'] = serializers.DateField(read_only=True)

	def get_pdf(self, instance):
		request = self.context['request']
		if instance.pdf:
			pdf_url = instance.pdf.serve().url
			return request.build_absolute_uri(pdf_url)
		return None

	def validate_fecha_operacion(self, fecha_operacion):

		"""
			Validacion de fecha_operacio
			Hoy en dia se puede cualquier fecha.
			Habria que agregar que no se pueden hacer con fecha anterior a un periodo cerrado
		"""
		
		return fecha_operacion
		

	def validate(self, data):
		"""
			Validacion de issued_date. 
			Solo se puede hacer en la validacion grupal para poder acceder a point_of_sales e issued_date juntos
			No se permite si
				Ya tiene un documento con fecha anterior a la solicitada
				10 dias anterior o posterior a la fecha actual
		"""

		if self.context['causante'] in ["cliente", "cliente-masivo"]:
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

		return data


		
	def create(self, validated_data):
		if self.context['sin_destinatario']:
			destinatario = None
			document_type = None
			document_number = None
		else:
			destinatario = validated_data['destinatario']
			document_type = destinatario.perfil.tipo_documento
			document_number = destinatario.perfil.numero_documento

		fecha_operacion = validated_data['fecha_operacion']
		descripcion = validated_data['descripcion']

		# Receipt
		receipt_data = validated_data['receipt']
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
		
		if self.context['comunidad'].contribuyente.certificate: # Si la comunidad tiene un certificado en el contribuyente de afip
			if destinatario: # Si el documento tiene destinatario
				if destinatario.naturaleza.nombre == "cliente" and self.context['receipt_type'].code in ['11', '12', '13']:
					receipt_data['afip'] = True
				
		
		receipt, receipt_afip = self.fields['receipt'].create(receipt_data)

		documento = Documento.objects.create(
			comunidad=self.context['comunidad'],
			receipt=receipt,
			receipt_afip=receipt_afip,
			destinatario=destinatario,
			fecha_operacion=fecha_operacion,
			descripcion=descripcion,
		)		
		documento.chequear_numeros()
		return documento