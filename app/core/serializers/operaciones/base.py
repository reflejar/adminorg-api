from rest_framework import serializers

from core.models import (
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
		self.fields['monto'] = serializers.DecimalField(decimal_places=2, max_digits=15)

	def display_vinculo(self, instance):
		if not instance:
			return ""
		return {
			'descripcion': ' - '.join([str(instance.cuenta), str(instance.concepto), str(instance.periodo())]),
			'monto': instance.saldo(fecha=self.context['fecha_operacion'])
		}