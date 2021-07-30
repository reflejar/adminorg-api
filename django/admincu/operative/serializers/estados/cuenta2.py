from django.admincu.operative.models.documento import Documento
from .base import *

class EstadoCuenta2Serializer(EstadoBaseSerializer):

	def __init__(self, queryset, context):
		super().__init__(queryset, context)
		self.saldo = Decimal(0.00) # Esto, una vez que se PAGINE, hay que hacer que no empiece en 0 sino en el saldo hasta el mov anterior del queryset
		self.orden = 0

	def makeJSON(self, d:Documento) -> Dict[str, Any]:

		operaciones = []
		for o in d.operaciones.all():
			if o.cuenta in d.cuenta.grupo:
				operaciones.append({
				'concepto': str(o.concepto()),
				'periodo': o.periodo(),
				'debe': o.debe,
				'haber': o.haber,
			})
			self.saldo = self.saldo + o.debe - o.haber

		return {
			'id': d.id,
			'fecha': d.operaciones[0].fecha,
			'nombre': "{} {}".format(d.receipt.receipt_type, d.receipt.formatted_number),
			'cuenta': "{}".format(d.destinatario),
			'causante': d.destinatario.naturaleza.nombre,
			'operaciones': operaciones,
			'valor': d.valor,
			'saldo': self.saldo
		}