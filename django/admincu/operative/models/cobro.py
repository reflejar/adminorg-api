from datetime import date
from django.db import models

from django_mercadopago.models import Payment as PaymentMP

from admincu.platforms.expensas_pagas.models import Payment as PaymentEP
from admincu.platforms.models import Plataforma
from admincu.utils.models import BaseModel
from admincu.operative.models import Documento

plataformas = {
	"mp": {
		"model": "PaymentMP"
	},
	'ep': {
		"model": "PaymentEP"
	}
}

class Cobro(BaseModel):
	"""
		Modelo de Documentos
		Representa los cobros realizados a traves de las plataformas habilitadas
			A la fecha: MercadoPago y ExpensasPagas
	"""

	fecha = models.DateField()
	plataforma = models.ForeignKey(Plataforma, on_delete=models.PROTECT, related_name="cobros_plataforma")
	payment_id = models.IntegerField()
	cliente = models.ForeignKey("operative.Cuenta", blank=True, null=True, on_delete=models.SET_NULL, related_name="cobros_plataforma")
	documento = models.ForeignKey(Documento, blank=True, null=True, on_delete=models.PROTECT, related_name="cobros_plataforma")
	valor = models.DecimalField(max_digits=9, decimal_places=2)

	def __str__(self):
		return self.plataforma.platform_code

	def cobro(self):
		return eval(plataformas[self.plataforma]['model']).objects.get(id=self.payment_id)

