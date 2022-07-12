from rest_framework import serializers

from adminsmart.apps.core.models import (
	Operacion,
	Cuenta
)


class OperacionModelSerializer(serializers.ModelSerializer):
	'''Operacion model serializer'''
	
	class Meta:
		model = Operacion

		fields = (
			'id',
			'detalle'
		)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['monto'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0.00)

	def display_vinculo(self, instance):
		return {
			'descripcion': ' - '.join([str(instance.cuenta), str(instance.concepto()), str(instance.periodo())]),
			'saldo': instance.saldo()
		}