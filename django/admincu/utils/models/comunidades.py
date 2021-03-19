from django.db import models
from django_afip.models import TaxPayer
# from django_mercadopago.models import Account


class TipoComunidad(models.Model):

	""" Modelo de tipos de comunidades """

	nombre = models.CharField(max_length=40)
	codigo_afip = models.CharField(max_length=4)

	def __str__(self):
		nombre = '%s' % (self.nombre)
		return nombre


class Comunidad(models.Model):

	contribuyente = models.ForeignKey(TaxPayer, on_delete=models.PROTECT, blank=True, null=True)
	nombre = models.CharField(max_length=200)
	domicilio = models.ForeignKey("utils.Domicilio", on_delete=models.PROTECT)
	tipo = models.ForeignKey(TipoComunidad, on_delete=models.PROTECT)
	abreviatura = models.CharField(max_length=7)
	mails = models.BooleanField(default=False)
	dominioweb = models.CharField(max_length=70, blank=True, null=True)
	costo_mp = models.BooleanField(default=False) # Si es True el club se hace cargo
	cierre = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.nombre
