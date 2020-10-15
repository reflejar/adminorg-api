from rest_framework import serializers
from admincu.files.models import (
	Carpeta,
	Archivo
)

class ArchivoModelSerializer(serializers.ModelSerializer):
	'''Archivo model serializer'''


	class Meta:
		model = Archivo

		fields = (
			'id',
			'nombre',
			'descripcion',
			'ubicacion'
		)    

	def __init__(self, *args, **kwargs):
		super(ArchivoModelSerializer, self).__init__(*args, **kwargs)
		self.fields['carpeta'] = serializers.PrimaryKeyRelatedField(queryset=Carpeta.objects.filter(comunidad=self.context['comunidad']), allow_null=True)
		

	def create(self, validate_data):
		archivo = Archivo.objects.create(
			**validate_data,
			comunidad = self.context['comunidad'],
		)
		return archivo
