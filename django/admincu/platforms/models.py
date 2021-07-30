from datetime import date
from django.db import models
from django_mercadopago.models import Account as AccountMP
from admincu.platforms.expensas_pagas.models import AccountEP
from admincu.platforms.simple_solutions.models import AccountSS

from admincu.utils.models import BaseModel




## DEPRACTAR


"""
	Medianamente en desuso puesto que los modelos de cada plataforma
	ya heredan de BaseModel asi que tienen comunidad y el registro de fechas
"""

plataformas = {
	"mp": {
		"nombre": "MercadoPago",
		"model": "AccountMP"
	},
	'ep': {
		"nombre": "ExpensasPagas",
		"model": "AccountEP"
	}, 
	'ss': {
		"nombre": "SimpleSolutions",
		"model": "AccountSS"
	}
}

CODE_CHOICES = [(k, v['nombre']) for k, v in plataformas.items()]

	
class Plataforma(BaseModel):
	platform_code = models.CharField(max_length=5, choices=CODE_CHOICES)
	app_id = models.IntegerField()

	def __str__(self):
		return plataformas[self.platform_code]['nombre']

	def cuenta(self):
		return eval(plataformas[self.platform_code]['model']).objects.get(id=self.app_id)

