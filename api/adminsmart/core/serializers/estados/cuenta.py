from .base import *


class EstadoCuentaSerializer(EstadoBaseSerializer):

	def __init__(self, queryset, context):
		super().__init__(queryset, context)
		self.saldo = Decimal(0.00)
		self.orden = 0

	def makeJSON(self, d:Documento) -> Dict[str, Any]:
		obj = self.context['cuenta']
		receipt_type = str(d.receipt.receipt_type)
		formatted_number = str(d.receipt.formatted_number)
		if isinstance(obj, Cuenta):
			total = sum([o.valor for o in d.operaciones.all() if o.cuenta in obj.grupo])
		else:
			total = sum([o.valor for o in d.operaciones.all() if o.cuenta.titulo in obj.grupo])
		self.saldo += total
		return {
			'id': d.id,
			'fecha': d.fecha_operacion,
			'causante': d.causante,
			'fecha_anulacion': d.fecha_anulacion,
			'nombre': receipt_type + " " + formatted_number,
			'receipt': {
				'receipt_type': receipt_type,
				'formatted_number': formatted_number
			},
			'total': total,
			'saldo': self.saldo
		}
