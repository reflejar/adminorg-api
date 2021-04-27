from rest_framework import serializers
from typing import Dict, Any

from admincu.operative.models import Operacion

"""

Este serializer es de tipo funcion por razones de optimizacion

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
		'naturaleza': operacion.cuenta.naturaleza.nombre,
		'valor': operacion.valor,
		'debe': operacion.debe(),
		'haber': operacion.haber(),
		# 'capital': operacion.,
		# 'interes': operacion,
		# 'total': operacion,		

	}
