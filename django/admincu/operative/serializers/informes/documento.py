from rest_framework import serializers

from admincu.operative.models import Documento

class DocumentoModelSerializer(serializers.ModelSerializer):
	
	'''Documento para la parte informes'''
	
	class Meta:
		model = Documento

		fields = (
			'id',
			'portador',
			'tipo',
			'numero'
		)
