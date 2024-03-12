from .base import *


class DescargaModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['cuenta'] = serializers.PrimaryKeyRelatedField(
				queryset=Cuenta.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza__nombre__in=["caja", "ingreso", "gasto"]
					), 
				allow_null=True
			)
		self.fields['fecha_vencimiento'] = serializers.DateField(allow_null=True)
