from rest_framework import serializers

from admincu.operative.models import Operacion
from admincu.operative.serializers.analitica import (
	CuentaModelSerializer,
	DocumentoModelSerializer,
	TituloModelSerializer
)

class AnaliticaModelSerializer(serializers.ModelSerializer):
	
	'''Operacion para la parte analitica'''

	cuenta = CuentaModelSerializer()
	documento = DocumentoModelSerializer()
	titulo = TituloModelSerializer()
	
	class Meta:
		model = Operacion

		fields = (
			'id',
			'detalle',
			'monto',
			'naturaleza',
			'cuenta',
			'titulo',
			'documento',
			'valor',
			'debe',
			'haber',
			'fecha',
			'fecha_indicativa',
			'cantidad',
			'fecha_vencimiento',
			'fecha_gracia',
			'detalle',
			'descripcion'
		)