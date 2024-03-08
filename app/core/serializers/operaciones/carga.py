from .base import *


class CargaModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		self.fields['cantidad'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0, allow_null=True)
		self.fields['periodo'] = serializers.DateField(label="Periodo")
		self.fields['fecha_vencimiento'] = serializers.DateField(allow_null=True, label="Vencimiento")
		self.fields['concepto'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre__in=["ingreso", "gasto", "caja"]
						).order_by(
							'nombre'
						), 
					allow_null=True
				)