from admincu.operative.serializers.operaciones.base import *


class CreditoModelSerializer(OperacionModelSerializer):
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = Operacion()._meta
		self.fields['cantidad'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0.01, allow_null=True)
		self.fields['periodo'] = serializers.ModelField(model_field=fields.get_field("fecha_indicativa"))
		self.fields['fecha_gracia'] = serializers.ModelField(model_field=fields.get_field("fecha_gracia"), allow_null=True)
		self.fields['fecha_vencimiento'] = serializers.ModelField(model_field=fields.get_field("fecha_vencimiento"), allow_null=True)
		if self.context['retrieve']:
			self.fields['destinatario'] = serializers.CharField(max_length=200, read_only=True)
			self.fields['concepto'] = serializers.CharField(max_length=200, read_only=True)
		else:
			self.fields['destinatario'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre__in=['cliente', 'dominio']
						), 
					allow_null=False
				)
			self.fields['concepto'] = serializers.PrimaryKeyRelatedField(
					queryset=Cuenta.objects.filter(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre__in=["ingreso", "caja"]
						), 
					allow_null=False
				)