from admincu.operative.models import Operacion

from rest_framework import serializers


class EstadoCuentaModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Operacion

		fields = (
			# 'numero',
			'fecha',
			'concepto',
			'documento',
			'debe',
			'haber',
			'saldo',
		)