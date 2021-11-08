from .base import *


class EstadoCuentaSerializer(EstadoBaseSerializer):

	def __init__(self, queryset, context):
		super().__init__(queryset, context)
		self.saldo = Decimal(0.00)
		self.orden = 0

	def makeJSON(self, d:Documento) -> Dict[str, Any]:
		cuenta = self.context['cuenta']
		receipt_type = str(d.receipt.receipt_type)
		formatted_number = str(d.receipt.formatted_number)
		operaciones=[]
		total = 0
		for o in d.operaciones.all():
			if o.cuenta in cuenta.grupo:
				operaciones.append(o)
				total += o.valor
		self.saldo += total

		return {
			'id': d.id,
			'fecha': d.fecha_operacion,
			'causante': d.causante,
			'fecha_anulacion': d.fecha_anulacion,
			'nombre': receipt_type + " " + formatted_number,
			'receipt': {
				'receipt_type': receipt_type,
				'formatted_number': formatted_number,
			},
			'operaciones': [{
				'cuenta': str(o.cuenta),
				'concepto': str(o.concepto()),
				'periodo': o.periodo(),
				'valor': o.valor,
			} for o in operaciones],
			'total': total,
			'saldo': self.saldo
		}
