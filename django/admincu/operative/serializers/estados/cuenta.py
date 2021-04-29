from .base import *
from django.db.models import Sum


class EstadoCuentaModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Cuenta
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields.pop('capital')
		self.fields.pop('valor')		
		self.fields.pop('monto')		
		self.fields.pop('interes')		
		self.fields.pop('total')		
		self.fields.pop('pago_capital')		
		self.orden = 0
		self.saldo = 0.00


	def get_saldo(self, obj):
		if self.orden == 0:
			self.saldo = Operacion.objects.filter(
				cuenta=obj.cuenta,
				fecha__lte=obj.fecha,
				id__lte=obj.id
			).aggregate(calculo=Sum('valor'))['calculo'] or 0
		else:
			self.saldo = self.saldo + obj.debe - obj.haber

		self.orden += 1

		return self.saldo


