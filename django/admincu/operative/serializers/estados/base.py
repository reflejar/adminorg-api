from admincu.operative.serializers.operaciones.base import *
from admincu.operative.serializers.documentos.base import DocumentoModelSerializer
# from .documento import DocumentoParaEstadoModelSerializer


class EstadoBaseModelSerializer(OperacionModelSerializer):
	"""
		Base de Operaciones para Estados
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		self.fields['fecha'] = serializers.ModelField(model_field=fields.get_field("fecha"))
		self.fields['periodo'] = serializers.CharField(max_length=10)
		self.fields['cuenta'] = serializers.CharField(max_length=200)
		self.fields['causante'] = serializers.CharField(max_length=200)
		self.fields['fecha_gracia'] = serializers.ModelField(model_field=fields.get_field("fecha_gracia"))
		self.fields['fecha_vencimiento'] = serializers.ModelField(model_field=fields.get_field("fecha_vencimiento"))
		self.fields['documento'] = DocumentoModelSerializer(read_only=True, context=self.context, many=False)
		# self.fields['documento'].fields.pop('destinatario')
		self.fields['documento'].fields.pop('fecha_operacion')
		self.fields['documento'].fields.pop('descripcion')
		self.fields['documento'].fields['receipt'].fields.pop('total_amount')
		self.fields['documento'].fields['receipt'].fields['formatted_number'] = serializers.CharField(max_length=150, read_only=True)