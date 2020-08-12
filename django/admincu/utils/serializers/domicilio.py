'''para crear serializer de domicilio en diferentes versiones
dependiendo de la extension necesaria para cada tipo de objeto'''

from rest_framework import serializers

from admincu.utils.models import Domicilio, Provincia


class DomicilioModelSerializer(serializers.ModelSerializer):
	'''Domicilio model serializer'''
	
	# provincia = serializers.ChoiceField(choices=list(Provincia.objects.all().values_list('nombre', flat=True)))

	class Meta:
		model = Domicilio
		fields = "__all__"