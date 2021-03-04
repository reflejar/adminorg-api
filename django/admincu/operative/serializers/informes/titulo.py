from rest_framework import serializers

from admincu.operative.models import Titulo

class TituloModelSerializer(serializers.ModelSerializer):
	
	'''Titulo para la parte informes'''
	
	class Meta:
		model = Titulo

		fields = (
			'id',
			'numero',
            'nombre'
		)