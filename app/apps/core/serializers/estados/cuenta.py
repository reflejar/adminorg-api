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
				saldo += q.valor
				q.saldo = saldo
			else:
				total = sum([o.valor for o in q.operaciones.all() if o.cuenta.titulo == obj])			
			queryset.append(q)

		self.queryset = list(queryset)[::-1]

	def makeJSON(self, o:Operacion) -> Dict[str, Any]:
		
		receipt_type = str(o.documento.receipt.receipt_type)
		formatted_number = str(o.documento.receipt.formatted_number)

		return {
			'fecha': o.fecha,
			'documento': {
				'id': o.documento.id,
				'fecha_anulacion': o.documento.fecha_anulacion,
				'receipt': {
					'receipt_type': receipt_type,
					'formatted_number': formatted_number
				},
				'nombre': receipt_type + " " + formatted_number,

			},
			'causante': o.documento.causante,
			'concepto': str(o.concepto or ''),
			'total': o.valor,
			'saldo': o.saldo
		}
