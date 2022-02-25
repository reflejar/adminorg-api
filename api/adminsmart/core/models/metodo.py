from django.db import models
from adminsmart.utils.models import BaseModel
from adminsmart.core.models import Naturaleza


class Metodo(BaseModel):

	"""
		Modelo de de metodos
        Representa metodos de calculo para diferentes cuestiones (intereses, descuentos, retenciones, amortizaciones)
        
	"""

	nombre = models.CharField(max_length=80)
	NATURALEZA_CHOICES = (
		('interes', 'Interes'),
		('descuento', 'Descuento'),
		('retencion', 'Retencion'),
	)
	naturaleza = models.CharField(max_length=15, choices=NATURALEZA_CHOICES)
	plazo = models.PositiveIntegerField(blank=True, null=True)

	FIJO = 'fijo'
	TASA = 'tasa'
	TIPO_CHOICES = (
			(FIJO, 'Monto fijo'),
			(TASA, 'Tasa')
		)
	tipo = models.CharField(max_length=15, choices=TIPO_CHOICES ,default=TASA)
	monto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	DIARIO = 1
	SEMANAL = 7
	QUINCENAL = 15
	MENSUAL = 30
	BIMESTRAL = 60
	TRIMESTRAL = 90
	SEMESTRAL = 120
	BASES_CHOICES = (
			(DIARIO, 'Diario'),
			(SEMANAL, 'Semanal'),
			(QUINCENAL, 'Quincenal'),
			(MENSUAL, 'Mensual'),
			(BIMESTRAL, 'Bimestral'),
			(TRIMESTRAL, 'Trimestral'),
			(SEMESTRAL, 'Semestral'),
		)
	reconocimiento = models.IntegerField(choices=BASES_CHOICES, default=DIARIO)
	base_calculo = models.IntegerField(choices=BASES_CHOICES, default=MENSUAL)

	CONDICION_CHOICES = (
			(None, 'Sin condicion'),
			('grupo', 'Pertenencia a un grupo'),
		)
	condicion = models.CharField(max_length=15, blank=True, null=True, choices=CONDICION_CHOICES)


	def __str__(self):
		return self.nombre