from .base import *


class EstadoCuentaSerializer(EstadoBaseSerializer):

	def __init__(self, queryset, context):
		super().__init__(queryset, context)
		# Esto hay que mejorar en pandas
		queryset = []
		saldo = Decimal(0.00)
		
		obj = self.context['cuenta']
		for q in list(self.queryset)[::-1]:
			if isinstance(obj, Cuenta):
				q.total = sum([o.valor for o in q.operaciones.all() if o.cuenta == obj])
				saldo += q.total
				q.saldo = saldo
			else:
				total = sum([o.valor for o in q.operaciones.all() if o.cuenta.titulo == obj])			
			queryset.append(q)

		self.queryset = list(queryset)[::-1]

	def makeJSON(self, d:Documento) -> Dict[str, Any]:
		
		receipt_type = str(d.receipt.receipt_type)
		formatted_number = str(d.receipt.formatted_number)

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
			'total': d.total,
			'saldo': d.saldo
		}
