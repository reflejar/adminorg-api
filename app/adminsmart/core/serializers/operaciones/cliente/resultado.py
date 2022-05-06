from adminsmart.core.serializers.operaciones.base import *


class ResultadoModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza__nombre__in=["ingreso", "gasto"]
					), 
				allow_null=False
			)
		self.fields['periodo'] = serializers.ModelField(model_field=fields.get_field("fecha_indicativa"))
