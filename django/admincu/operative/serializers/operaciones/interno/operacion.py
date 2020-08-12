from admincu.operative.serializers.operaciones.base import *


class LineaModelSerializer(OperacionModelSerializer):
	'''Operacion de debito realizada con proveedores'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		kwargs = {
			'comunidad': self.context['comunidad'], 
		}		
		if self.context['receipt_type'].code == "303":
			kwargs.update({
				'naturaleza__nombre': "caja"
			})
		cuentas = Cuenta.objects.filter(**kwargs)
		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=cuentas, 
				allow_null=False
			)