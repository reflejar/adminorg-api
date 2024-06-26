from django.db import models
from django_afip.models import CurrencyType


from utils.models import (
	BaseModel,
	Domicilio,
)
from core.models import (
	Titulo,
	Naturaleza,
	Taxon,
)

class Cuenta(BaseModel):

	"""
		Modelo de cuentas
		Representa todos los objetos que interactuan como cuenta contable y administrativa
		En algunos casos es cuenta y en otros es subcuenta: A traves de "nivel"
	"""

	titulo = models.ForeignKey(Titulo, on_delete=models.PROTECT) # El ordenamiento contable
	naturaleza = models.ForeignKey(Naturaleza, on_delete=models.PROTECT) # Para definir el modulo en que se utiliza
	taxon = models.ForeignKey(Taxon, blank=True, null=True, on_delete=models.PROTECT) # Para definir una caracterizacion
	moneda = models.ForeignKey(CurrencyType, blank=True, null=True, on_delete=models.PROTECT) # Moneda por defecto
	domicilio = models.ForeignKey(Domicilio, blank=True, null=True, on_delete=models.PROTECT)
	nombre = models.CharField(max_length=150, blank=True, null=True)
	perfil = models.ForeignKey("users.Perfil", blank=True, null=True, on_delete=models.SET_NULL)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		if self.perfil:
			if self.perfil.razon_social:
				return self.perfil.razon_social
			return self.perfil.nombre
		return self.nombre

	@property
	def direccion(self):
		return 1 if str(self.titulo.numero)[0] in ["1", "5"] else -1
	