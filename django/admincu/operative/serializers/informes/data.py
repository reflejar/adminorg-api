from rest_framework import serializers
from typing import Dict, Any

from admincu.operative.models import Operacion

"""

Este serializer es de tipo funcion por razones de optimizacion

"""

def InformesModelSerializer(o: Operacion) -> Dict[str, Any]:
	print(o)
	return {
		'fecha': o.fecha,
		'titulo_numero': o.cuenta.titulo.numero,
		'titulo_nombre': o.cuenta.titulo.nombre,
		'cuenta': str(o.cuenta),
		'concepto': str(o.concepto()),
		'periodo': o.periodo(),
		'documento_tipo': o.documento.receipt.receipt_type.description,
		'documento_numero': o.documento.receipt.formatted_number,
		'cantidad': o.cantidad,
		'naturaleza': o.cuenta.naturaleza.nombre,
		'valor': o.valor,
		'debe': o.debe,
		'haber': o.haber,
	}
