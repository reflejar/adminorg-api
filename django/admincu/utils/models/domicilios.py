from django.db import models

class Provincia(models.Model):
	nombre = models.CharField(max_length=40)
	codigo_afip = models.CharField(max_length=4)

	def __str__(self):
		nombre = '%s' % (self.nombre)
		return nombre

class Domicilio(models.Model):

	"""
		Tabla de Domicilios
		Se utiliza en diversos modelos
	"""

	provincia = models.ForeignKey(Provincia, blank=True, null=True, on_delete=models.PROTECT)
	localidad = models.CharField(max_length=70, blank=True, null=True)
	calle = models.CharField(max_length=70, blank=True, null=True)
	numero = models.CharField(max_length=10, blank=True, null=True)
	piso = models.CharField(max_length=10, blank=True, null=True)
	oficina = models.CharField(max_length=10, blank=True, null=True)
	sector = models.CharField(max_length=10, blank=True, null=True)
	torre = models.CharField(max_length=10, blank=True, null=True)
	manzana = models.CharField(max_length=10, blank=True, null=True)
	parcela = models.CharField(max_length=10, blank=True, null=True)
	catastro = models.CharField(max_length=10, blank=True, null=True)

	superficie_total = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
	superficie_cubierta = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)

	def __str__(self):

		return self.calle

