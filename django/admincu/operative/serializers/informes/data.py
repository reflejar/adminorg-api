from rest_framework import serializers
from typing import Dict, Any

from admincu.operative.models import Operacion
# from admincu.operative.serializers.operaciones.calculator import *

"""

Hacer que herede de OperacionModelSerializer
que OperacionModelSerializer tenga todos los calculos.
Inspeccionar que pasa con sobreescribir las cosas


"""

def InformesModelSerializer(operacion: Operacion) -> Dict[str, Any]:
	concepto = operacion.concepto()
	return {
		'fecha': operacion.fecha,
		'titulo_numero': operacion.cuenta.titulo.numero,
		'titulo_nombre': operacion.cuenta.titulo.nombre,
		'cuenta': str(operacion.cuenta),
		'concepto': str(concepto) if concepto else None,
		'periodo': operacion.fecha_indicativa,
		'documento_tipo': operacion.documento.receipt.receipt_type.description,
		'documento_numero': operacion.documento.receipt.formatted_number,
		'cantidad': operacion.cantidad,
		'monto': operacion.monto(),
		'debe': operacion.debe(),
		'haber': operacion.haber(),
		# 'capital': operacion.,
		# 'interes': operacion,
		# 'total': operacion,		

	}

# class InformesModelSerializer(CalculatorModelSerializer):
	
# 	'''Operacion para la parte informes'''

# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.fields.pop('pago_capital')
# 		# Si se decide que se exporte el SALDO, INTERES y TOTAL, se tiene que buscar una buena forma 
# 		# que no tome tanto tiempo de calculo
# 		self.fields.pop('saldo')
# 		self.fields.pop('interes')
# 		self.fields.pop('total')