from .base import *


class EstadoCuentaSerializer(EstadoBaseSerializer):

	def __init__(self, queryset, context):
		super().__init__(queryset, context)
		self.saldo = Decimal(0.00)
		self.orden = 0

	def makeJSON(self, o:Operacion) -> Dict[str, Any]:
		self.saldo += o.valor

		receipt_type = str(o.documento.receipt.receipt_type)
		formatted_number = str(o.documento.receipt.formatted_number)

		return {
			'id': o.id,
			'fecha': o.fecha,
			'causante': o.causante(),
			'documento': {
				'id': o.documento.id,
				'fecha_anulacion': o.documento.fecha_anulacion,
				'receipt': {
					'receipt_type': receipt_type,
					'formatted_number': formatted_number,
				},
				'nombre': receipt_type + " " + formatted_number
			}, 
			'cuenta': str(o.cuenta),
			'concepto': str(o.concepto()),
			'periodo': o.periodo(),
			'debe': o.debe,
			'haber': o.haber,
			'saldo': self.saldo
		}