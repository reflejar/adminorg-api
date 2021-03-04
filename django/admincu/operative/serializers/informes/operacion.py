from rest_framework import serializers

from admincu.operative.models import Operacion
from admincu.operative.serializers.informes import (
	CuentaModelSerializer,
	DocumentoModelSerializer,
	TituloModelSerializer
)

class InformesModelSerializer(serializers.ModelSerializer):
	
	'''Operacion para la parte informes'''

	cuenta = CuentaModelSerializer()
	documento = DocumentoModelSerializer()
	titulo = TituloModelSerializer()
	saldo = serializers.SerializerMethodField()
	
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
			'descripcion',
			'saldo'
		)

	def get_saldo(self, obj):

		return obj.saldo(fecha=self.context['end_date'])