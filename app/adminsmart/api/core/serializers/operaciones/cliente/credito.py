from adminsmart.api.core.serializers.operaciones.base import *


class CreditoModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		self.fields['cantidad'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0, allow_null=True)
		self.fields['fecha_indicativa'] = serializers.DateField(label="Periodo")
		self.fields['fecha_gracia'] = serializers.DateField(allow_null=True, label="Descuento")
		self.fields['fecha_vencimiento'] = serializers.DateField(allow_null=True, label="Vencimiento")
		if 'retrieve' in self.context.keys():
			self.fields['destinatario'] = serializers.CharField(max_length=200, read_only=True)
			self.fields['concepto'] = serializers.CharField(max_length=200, read_only=True)
		else:
			self.fields['destinatario'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre__in=['cliente', 'dominio'],
							id__in=self.context['cuenta'].grupo.all().values('id')
						), 
					allow_null=True,
				)
			self.fields['concepto'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre__in=["ingreso", "caja"]
						).order_by(
							'nombre'
						), 
					allow_null=True
				)