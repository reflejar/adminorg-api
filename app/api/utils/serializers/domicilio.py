'''para crear serializer de domicilio en diferentes versiones
dependiendo de la extension necesaria para cada tipo de objeto'''

from rest_framework import serializers

from apps.utils.models import Domicilio, Provincia

try:
	PROVINCIAS_CHOICES = list(Provincia.objects.all().values_list('nombre', flat=True))
except:
	PROVINCIAS_CHOICES = []

class DomicilioModelSerializer(serializers.ModelSerializer):
	'''Domicilio model serializer'''
	
	provincia = serializers.ChoiceField(choices=PROVINCIAS_CHOICES)

	class Meta:
		model = Domicilio
		fields = "__all__"