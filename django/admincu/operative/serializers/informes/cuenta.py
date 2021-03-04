from rest_framework import serializers

from admincu.operative.models import Cuenta

class CuentaModelSerializer(serializers.ModelSerializer):
	
	'''Cuenta para la parte informes'''

	nombre = serializers.SerializerMethodField()
	
	class Meta:
		model = Cuenta

		fields = (
			'id',
			'nombre',
		)


	def get_nombre(self, obj):
		return str(obj)