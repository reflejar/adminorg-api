from apps.core.serializers.operaciones.base import *
from apps.core.serializers.documentos.base import DocumentoModelSerializer


class DebitoModelSerializer(OperacionModelSerializer):
	'''Operacion de debito realizada con proveedores'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		
		self.fields['cantidad'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0.01, allow_null=True)
		self.fields['fecha_vencimiento'] = serializers.ModelField(model_field=fields.get_field("fecha_vencimiento"), allow_null=True)

		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza__nombre__in=["caja", "gasto", "bien_de_cambio", "bien_de_uso"]
					), 
				allow_null=False
			)
		
		if 'retrieve' in self.context.keys():
			self.fields['documento'] = DocumentoModelSerializer(read_only=True, context=self.context, many=False)
			self.fields['documento'].fields.pop('destinatario')
			self.fields['documento'].fields.pop('fecha_operacion')
			self.fields['documento'].fields.pop('descripcion')
			self.fields['documento'].fields['receipt'].fields.pop('total_amount')
			self.fields['documento'].fields['receipt'].fields['formatted_number'] = serializers.CharField(max_length=150, read_only=True)



