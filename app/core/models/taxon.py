from django.db import models

class Taxon(models.Model):
	naturaleza = models.ForeignKey("core.Naturaleza", related_name="taxones", on_delete=models.PROTECT)
	nombre = models.CharField(max_length=100)

	def __str__(self):

		return self.nombre

