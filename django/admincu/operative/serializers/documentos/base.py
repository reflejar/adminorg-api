from rest_framework import serializers

from admincu.operative.models import (
	Documento,
	Cuenta
)
from admincu.operative.serializers import ReceiptModelSerializer

from django_afip.models import (
	Receipt,
	ReceiptType,
	PointOfSales,
	ConceptType,
	DocumentType,
	CurrencyType
)


class DocumentoModelSerializer(serializers.ModelSerializer):
	'''Documento model serializer'''
	
	class Meta:
		model = Documento

		fields = (
			'id',
			'fecha_operacion',
			'descripcion',
		)
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Fields comunes:
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


	def validate_fecha_operacion(self, fecha_operacion):

		"""
			Validacion de fecha_operacio
			Hoy en dia se puede cualquier fecha.
			Habria que agregar que no se pueden hacer con fecha anterior a un periodo cerrado
		"""
		
		return fecha_operacion
		
		
	def create(self, validated_data):
		if self.context['sin_destinatario']:
			destinatario = None
			document_type = DocumentType.objects.get(code=80)
			document_number = self.context['comunidad'].contribuyente.cuit
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
			'concept': ConceptType.objects.get(description="productos y servicios")
		})
		# if not 'concept' in receipt_data.keys():
		# 	receipt_data['concept'] = ConceptType.objects.get(description="servicios")

		if self.context['comunidad'].contribuyente.certificate: # Si la comunidad tiene un certificado en el contribuyente de afip
			if destinatario: # Si el documento tiene destinatario
				if destinatario.naturaleza.nombre == "cliente" and self.context['receipt_type'].code in ['11', '12', '13']:
					receipt_data['afip'] = True
				
		
		receipt = self.fields['receipt'].create(receipt_data)

		documento = Documento.objects.create(
			comunidad=self.context['comunidad'],
			receipt=receipt,
			destinatario=destinatario,
			fecha_operacion=fecha_operacion,
			descripcion=descripcion,
		)		
		return documento