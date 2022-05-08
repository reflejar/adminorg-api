from adminsmart.api.core.serializers.operaciones.base import *


class CargaModelSerializer(OperacionModelSerializer):
	'''Operacion de debito realizada con proveedores'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta

		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza__nombre__in=["caja"]
					), 
				allow_null=False
			)