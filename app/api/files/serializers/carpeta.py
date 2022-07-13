from rest_framework import serializers
from django.contrib.auth.models import Group

from apps.files.models import Carpeta
from api.files.serializers import ArchivoModelSerializer

class CarpetaModelSerializer(serializers.ModelSerializer):

	'''Carpeta model serializer'''


	class Meta:
		model = Carpeta

		fields = (
			'id',
			'nombre',
			'descripcion',
			'supercarpeta',
		)    


	def __init__(self, *args, **kwargs):
		super(CarpetaModelSerializer, self).__init__(*args, **kwargs)
		self.fields['archivos'] = ArchivoModelSerializer(context=self.context, read_only=True, many=True)
		exposicion_choices = Group.objects.all().values_list('name', flat=True)
		# self.fields['exposicion'] = serializers.MultipleChoiceField(
		# 		required=True, 
		# 		choices=exposicion_choices
		# 	)
		


	def validate_nombre(self, nombre):
		"""
			No puede haber carpetas con el mismo nombre 
		"""

		query = Carpeta.objects.filter(
				comunidad=self.context['comunidad'], 
				nombre=nombre
			)

		if query:
			if self.context['request'].method == 'POST' or not self.instance in query:
				raise serializers.ValidationError('Ya existe un carpeta con el nombre solicitado')

		return nombre

	def validate_exposicion(self, exposicion):
		"""
			Solo para convertir en objeto
		"""

		return Group.objects.filter(name__in=exposicion)		



	def create(self, validate_data):
		# exposiciones = validate_data.pop('exposicion')
		carpeta = Carpeta.objects.create(
			**validate_data,
			comunidad = self.context['comunidad'],
		)
		# for exposicion in exposiciones:
		# 	carpeta.exposicion.add(exposicion)

		return carpeta
