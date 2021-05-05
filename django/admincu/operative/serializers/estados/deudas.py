from .base import *

class EstadoDeudasSerializer(EstadoBaseSerializer):


	def saldo(self, monto, pago_capital, interes, descuento):

		return monto - pago_capital + interes - descuento

	def makeJSON(self, o:Operacion) -> Dict[str, Any]:


		pago_capital = o.pago_capital(fecha=self.context['end_date'])
		interes = o.interes(fecha=self.context['end_date'], condonacion=self.context['condonacion'])
		descuento = o.descuento(fecha=self.context['end_date'], condonacion=self.context['condonacion'])

		receipt_type = str(o.documento.receipt.receipt_type)
		formatted_number = str(o.documento.receipt.formatted_number)

		return {
			'id': o.id,
			'fecha': o.fecha,
			'causante': o.naturaleza,
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
			'monto': o.monto,
			'pago_capital': pago_capital,
			'interes': interes,
			'saldo': self.saldo(o.monto, pago_capital, interes, descuento)
		}