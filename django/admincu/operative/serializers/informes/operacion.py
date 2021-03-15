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
	concepto = serializers.SerializerMethodField()
	
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
			'concepto',
			'periodo',
			'cantidad',
			'fecha_vencimiento',
			'fecha_gracia',
			'detalle',
			'descripcion',
			'saldo'
		)

	def get_saldo(self, obj):

		return {
			'capital': obj.saldo(condonacion=True),
			'interes': obj.interes(fecha=self.context['end_date']),
			'total': obj.saldo(fecha=self.context['end_date'])
		}

	def get_concepto(self, obj):
		if obj.concepto():
			return str(obj.concepto())
		return None		