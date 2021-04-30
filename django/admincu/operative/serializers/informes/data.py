from rest_framework import serializers
from typing import Dict, Any

from admincu.operative.models import Operacion

"""

Este serializer es de tipo funcion por razones de optimizacion

"""

def InformesModelSerializer(o: Operacion) -> Dict[str, Any]:
	c = str(o.concepto())
	print(o)
	return {
		'fecha': o.fecha,
		'titulo_numero': o.cuenta.titulo.numero,
		'titulo_nombre': o.cuenta.titulo.nombre,
		'cuenta': str(o.cuenta),
		'concepto': c,
		'periodo': o.periodo(),
		'documento_tipo': o.documento.receipt.receipt_type.description,
		'documento_numero': o.documento.receipt.formatted_number,
		'cantidad': o.cantidad,
		'naturaleza': o.cuenta.naturaleza.nombre,
		'valor': o.valor,
		'debe': o.debe,
		'haber': o.haber,
		# 'capital': o.,
		# 'interes': o,
		# 'total': o,		

	}


# class InformesModelSerializer(serializers.ModelSerializer):
# 	'''Operacion model serializer'''
	
# 	class Meta:
# 		model = Operacion

# 		fields = (
# 			'fecha',
# 			'detalle',
# 			'cantidad',
# 			'naturaleza',
# 			'periodo',
# 			'valor',
# 			'debe',
# 			'haber',
# 			'titulo_numero',
# 			'titulo_nombre',
# 			'documento_tipo',
# 			'documento_numero'

# 		)
# 		read_only_fields = fields

# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.fields['cuenta'] = serializers.CharField(max_length=10)
# 		self.fields['concepto'] = serializers.CharField(max_length=10)