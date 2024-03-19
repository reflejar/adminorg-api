from rest_framework import serializers
from core.models import Proyecto

class ProyectoModelSerializer(serializers.ModelSerializer):
	"""
		Serializer particular de Cuenta para Contabilidad
	"""

	class Meta:
		model = Proyecto

		fields = (
			'id',
			'nombre'
		)
	

	def create(self, validate_data):
		proyecto = Proyecto.objects.create(
			**validate_data,
			comunidad = self.context['comunidad'],
		)
		return proyecto
