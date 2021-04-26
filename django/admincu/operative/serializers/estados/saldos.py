from .base import *


class EstadoSaldosModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Saldos a Favor
	"""


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields.pop('capital')
		self.fields.pop('valor')		
		self.fields.pop('debe')
		self.fields.pop('haber')
		self.fields.pop('total')
		self.fields.pop('pago_capital')

