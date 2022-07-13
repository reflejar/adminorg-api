from django.db import models
from apps.utils.models import (
	BaseModel,
)
from apps.core.models import (
	Taxon,
	Metodo,
)


class Grupo(BaseModel):

	"""
		Modelo de grupos
		Representa las agrupaciones posibles por tipo (taxon) con metodos (de descuento por ejemplo)
		Definicion de tipos:
			Equipos (Lo poseen todos los que pertenezcan)
			Categorias en clubes deportivos (Lo poseen todos los que pertenezcan)
			Familias (Solo lo posee el cabeza)
			Proveedores 
	"""
	
	nombre = models.CharField(max_length=150)
	descripcion = models.TextField(blank=True, null=True)
	taxon = models.ForeignKey(Taxon, on_delete=models.PROTECT) # Tipo de grupo
	metodos = models.ManyToManyField(Metodo, blank=True) # Por si tiene algun metodo de intereses o descuentos
	edad_limite = models.PositiveIntegerField(blank=True, null=True)
	cantidad_limite = models.PositiveIntegerField(blank=True, null=True)
	grupo_siguiente = models.ForeignKey('self', blank=True, null=True, related_name="grupo_anterior", on_delete=models.SET_NULL)

	def __str__(self):
		return self.nombre