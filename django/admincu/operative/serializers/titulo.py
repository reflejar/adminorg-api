from rest_framework import serializers
from admincu.operative.models import (
	Titulo,
)


class TituloModelSerializer(serializers.ModelSerializer):
	'''Titulo model serializer'''

	class Meta:
		model = Titulo

		fields = (
			'id',
			'nombre',
		)    


	def validate_nombre(self, nombre):
		"""
			No puede haber titulos con el mismo nombre 
		"""

		query = Titulo.objects.filter(
				comunidad=self.context['comunidad'], 
				nombre=nombre
			)

		if query:
			if self.context['request'].method == 'POST' or not self.instance in query:
				raise serializers.ValidationError('Ya existe un {} con el nombre solicitado'.format(self.context['naturaleza']))

		return nombre		


	def create(self, validate_data):
		titulo = Titulo.objects.create(
			**validate_data,
			comunidad = self.context['comunidad'],
		)
		return titulo
