from django.db import models


class Modulo(models.Model):
	handler = models.CharField(max_length=40)
	nombre = models.CharField(max_length=70)
	icon = models.CharField(max_length=70)
	path = models.CharField(max_length=70)

	def __str__(self):
		nombre = '%s' % (self.nombre)
		return nombre