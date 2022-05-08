from adminsmart.api.core.serializers.operaciones.base import *


class LineaModelSerializer(OperacionModelSerializer):
	'''Operacion de debito realizada con proveedores'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(comunidad=self.context['comunidad']), 
				allow_null=False
			)