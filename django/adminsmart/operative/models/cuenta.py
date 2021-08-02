from datetime import date
from itertools import chain
from django.db import models
from django.apps import apps

from adminsmart.utils.models import (
	BaseModel,
	Domicilio,
)
from adminsmart.operative.models import (
	Titulo,
	Naturaleza,
	Taxon,
	Metodo,
	Grupo,
)
from adminsmart.users.models import Perfil

class Cuenta(BaseModel):

	"""
		Modelo de cuentas
		Representa todos los objetos que interactuan como cuenta contable y administrativa
		En algunos casos es cuenta y en otros es subcuenta: A traves de "nivel"
	"""

	titulo = models.ForeignKey(Titulo, on_delete=models.PROTECT) # El ordenamiento contable
	naturaleza = models.ForeignKey(Naturaleza, on_delete=models.PROTECT) # Para definir el modulo en que se utiliza
	taxon = models.ForeignKey(Taxon, blank=True, null=True, on_delete=models.PROTECT) # Para definir una caracterizacion
	grupos = models.ManyToManyField(Grupo, blank=True) # Para definir cualquier tipo de grupo
	domicilio = models.ForeignKey(Domicilio, blank=True, null=True, on_delete=models.PROTECT)
	numero = models.IntegerField(blank=True, null=True)
	nombre = models.CharField(max_length=150, blank=True, null=True)
	slug = models.CharField(max_length=150, blank=True, null=True)
	perfil = models.ForeignKey("users.Perfil", blank=True, null=True, on_delete=models.SET_NULL)
	vinculos = models.ManyToManyField("self", through='DefinicionVinculo', blank=True, symmetrical=False) #agregar vonculacion 'mediante'
	metodos = models.ManyToManyField(Metodo, blank=True)

	def __str__(self):
		nombre = ""
		if self.perfil:
			nombre += "{}".format(str(self.perfil)) 
		else:
			nombre += "{}".format(self.nombre if self.nombre else self.numero) 
		return nombre

	@property
	def grupo(self):
		"""
			Grupo de el socio con sus dominios
		"""
		grupo = self.vinculos.filter(vinculo2__definicion__nombre="propietario")
		grupo |= Cuenta.objects.filter(id=self.id)
		return grupo

	def get_model(self, nombre):
		return apps.get_model('operative', nombre)

	def estado_deuda(self, fecha=None):
		fecha = fecha if fecha else date.today()
		kwargs = {
			'cuenta__in': self.grupo,
			'vinculo__isnull': True,
			'documento__isnull': False,
			'documento__fecha_anulacion__isnull': True
		}
		if self.naturaleza.nombre in ['cliente', 'caja']:
			kwargs.update({'valor__gt': 0})
			if self.naturaleza.nombre == 'caja':
				kwargs.update({'cuenta__taxon__nombre': 'stockeable'})				
		else:
			kwargs.update({'valor__lt': 0})
		deudas = self.get_model('Operacion').objects.filter(**kwargs)
		excluir = []
		for d in deudas:
			# if d.saldo(fecha=fecha) <= 0: # Esta es la logica para consultar CUANTO SE DEBIA A UNA FECHA
			if d.saldo() <= 0.00: # Esta es la logica para consultar CUANTO SE DEBIA A UNA FECHA pero excluyendo las pagadas posteriormente
				excluir.append(d.id)
		
		return deudas.exclude(id__in=excluir).order_by('fecha', 'id')


	def estado_cuenta(self, fecha=None):	
		fecha = fecha if fecha else date.today()
		return self.get_model('Operacion').objects.filter(
				cuenta__in=self.grupo, 
				# fecha__lte=fecha,
				documento__isnull=False,
			).select_related(
				"cuenta", 
				"cuenta__perfil", # Para el nombre de la cuenta
				"cuenta__naturaleza",
				"documento__destinatario",
				"documento__destinatario__naturaleza",
				"documento__receipt", 
				"documento__receipt__receipt_type", 
				"vinculo",
			).prefetch_related(
				"vinculos",
				"vinculos__cuenta",
				"vinculos__cuenta__naturaleza",
				"vinculo__vinculos",
				"vinculo__vinculos__cuenta",
				"vinculo__vinculos__cuenta__naturaleza",
			).order_by('fecha', 'id')

		
	def estado_saldos(self, fecha=None):
		fecha = fecha if fecha else date.today()
		kwargs = {
			'cuenta': self,
			'vinculo__isnull': True,
			'documento__isnull': False,
			'documento__fecha_anulacion__isnull': True
		}
		if self.naturaleza.nombre in ['cliente', 'caja']:
			kwargs.update({'valor__lt': 0})
			if self.naturaleza.nombre == 'caja':
				kwargs.update({'cuenta__taxon__nombre': 'stockeable'})				
		else:
			kwargs.update({'valor__gt': 0})
		saldos = self.get_model('Operacion').objects.filter(**kwargs)
		excluir = []
		for s in saldos:
			if s.saldo(fecha=fecha) <= 0:
				excluir.append(s.id)
		return saldos.exclude(id__in=excluir).order_by('-fecha', '-id')

	def vinculaciones(self):
		return self.vinculo1.all()

	def propietario(self):
		"""Retorna la Cuenta de Cliente que es propietario de un dominio"""
		try:
			return self.vinculo2.get(definicion__nombre='propietario').cuenta
		except:
			return

	def inquilino(self):
		"""Retorna la Cuenta de Cliente que es inquilino de un dominio"""
		try:
			return self.vinculo2.get(definicion__nombre='inquilino').cuenta
		except:
			return

	def descuento(self):
		"""Retorna el Metodo de descuento vigente"""
		try:
			return self.metodos.get(naturaleza="descuento")
		except:
			return
	
	def interes(self):
		"""Retorna el Metodo de interes vigente"""
		try:
			return self.metodos.get(naturaleza="interes")
		except:
			return					

	def retiene(self):
		"""Retorna los Metodos de retencion que se le aplican a una Cuenta de Proveedor"""
		return self.metodos.filter(naturaleza="retencion")

class DefinicionVinculo(models.Model):
	'''Hoy en dia esta tabla es solamente para vincular dominios con socios'''
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='vinculo1') #Socio
	cuenta_vinculada = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='vinculo2') #Dominio
	definicion = models.ForeignKey(Taxon, on_delete=models.PROTECT) #Tipo de relacion
	boolean = models.BooleanField(default=False) #Sin utilidad por ahora
