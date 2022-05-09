from rest_framework import serializers

from adminsmart.apps.core.models import Operacion


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