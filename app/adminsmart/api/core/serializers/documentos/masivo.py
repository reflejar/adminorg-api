from django.db import transaction

from adminsmart.core.models import Operacion
from adminsmart.core.CU.operaciones.clientes import masivo as operacionesMasivo

from .base import *
from .cliente import DestinoClienteModelSerializer

class DistribucionSerializer(serializers.Serializer):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['ingreso'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'],
						naturaleza__nombre="ingreso"
					),
				allow_null=False
			)
		unidades_choices = {
			'socio': "Total por socio",
			'dominio': "Total por dominio",
			'm2': "Total por m2",
		}
		self.fields['unidad'] = serializers.ChoiceField(choices=unidades_choices)
		self.fields['fecha_gracia'] = serializers.DateField(allow_null=True)
		self.fields['fecha_vencimiento'] = serializers.DateField(allow_null=True)
		self.fields['monto'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0.01)


class MasivoClienteModelSerializer(DocumentoModelSerializer):
	'''Documento con destino a cliente model serializer'''


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['distribuciones'] = DistribucionSerializer(read_only=False, many=True, context=self.context)

		self.fields['preconceptos'] = serializers.PrimaryKeyRelatedField(
				queryset=Operacion.objects.filter(
					comunidad=self.context['comunidad'],
					documento__isnull=True,
					fecha__isnull=True,
					cuenta__naturaleza__nombre__in=["cliente", "dominio"],
				), many=True
			)


	@transaction.atomic
	def create(self, validated_data):
		documento = Documento(
			comunidad=self.context['comunidad'],
			fecha_operacion=validated_data['fecha_operacion'],
		)
		list_of_docs = operacionesMasivo.CU(documento, validated_data).create()
		# self.hacer_pdfs(list_of_docs)
		# self.send_emails(list_of_docs)
		return list_of_docs

	def hacer_pdfs(self, list_of_docs):
		documentos = Documento.objects.filter(id__in=list_of_docs)
		for d in documentos:
			d.hacer_pdf()

	def send_emails(self, list_of_docs):
		for d in Documento.objects.filter(id__in=list_of_docs):
			documento = DestinoClienteModelSerializer(instance=d)
			documento.send_email(d)



