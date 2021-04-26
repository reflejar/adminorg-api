from .base import *


class EstadoDeudasModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Deuda
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields.pop('capital')
		self.fields.pop('valor')
		self.fields.pop('debe')
		self.fields.pop('haber')
		self.fields.pop('total')

	def get_interes(self, obj):

		return obj.interes(fecha=self.context['end_date'], condonacion=self.context['condonacion'])			

	def get_saldo(self, obj):

		return obj.saldo(fecha=self.context['end_date'], condonacion=self.context['condonacion'])	

	def get_pago_capital(self, obj):

		return obj.pago_capital(fecha=self.context['end_date'])