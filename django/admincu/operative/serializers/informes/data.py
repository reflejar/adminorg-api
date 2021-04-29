from rest_framework import serializers
from typing import Dict, Any

from admincu.operative.models import Operacion

"""

Este serializer es de tipo funcion por razones de optimizacion

"""

def InformesModelSerializer(o: Operacion) -> Dict[str, Any]:
	c = o.concepto()
	r = o.documento.receipt
	t = o.cuenta.titulo
	print(o)
	return {
		'fecha': o.fecha,
		'titulo_numero': t.numero,
		'titulo_nombre': t.nombre,
		'cuenta': o.destinatario(),
		'concepto': str(c) if c else None,
		'periodo': o.fecha_indicativa,
		'documento_tipo': r.receipt_type.description,
		'documento_numero': r.formatted_number,
		'cantidad': o.cantidad,
		'naturaleza': o.naturaleza,
		'valor': o.valor,
		'debe': o.debe,
		'haber': o.haber,
		# 'capital': o.,
		# 'interes': o,
		# 'total': o,		

	}
