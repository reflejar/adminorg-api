from apps.core.serializers.operaciones.base import *


class CajaModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza__nombre="caja"
					), 
				allow_null=False
			)
		self.fields['fecha_vencimiento'] = serializers.DateField(allow_null=True)
