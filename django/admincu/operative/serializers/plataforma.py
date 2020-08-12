from django.db import transaction
from rest_framework import serializers

from admincu.operative.models import (
	Cobro,
    Cuenta
)


class CobroPlataformaModelSerializer(serializers.ModelSerializer):
	"""
		Serializer de Cobro de plataforma
	"""
	
	class Meta:
		model = Cobro

		fields = (
			'id',
			'fecha',
            'cliente',
            'valor'
		)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['plataforma'] = serializers.CharField(max_length=150)