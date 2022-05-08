from rest_framework import serializers

from adminsmart.core.models import (
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