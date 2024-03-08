from datetime import date
import pandas as pd
from itertools import chain
from django.db import models
from django.apps import apps
from django.db.models import F, Sum, Window
from django_pandas.io import read_frame

from apps.utils.models import (
	BaseModel,
	Domicilio,
)
from apps.core.models import (
	Titulo,
	Naturaleza,
	Taxon,
	Metodo,
	Grupo,
)
from apps.users.models import Perfil

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
	is_active = models.BooleanField(default=True)

	def __str__(self):
					# else '#' + str(int(x['CUENTA_NUMERO'])) if x['NATURALEZA'] in ['dominio'] \
					# else x['CUENTA_NOMBRE'], 
		if self.perfil:
			if self.perfil.razon_social:
				return self.perfil.razon_social
			return ', '.join([self.perfil.apellido, self.perfil.nombre])
		if self.numero:
			return f"#{self.numero}"
		return self.nombre

	@property
	def grupo(self):
		"""
			Grupo de el socio con sus dominios
		"""
		grupo = self.vinculos.filter(vinculo2__definicion__nombre="propietario")
		grupo |= Cuenta.objects.filter(id=self.id)
		return grupo

	@staticmethod
	def get_model(nombre):
		return apps.get_model('operative', nombre)

	@property
	def direccion(self):
		return 1 if str(self.titulo.numero)[0] in ["1", "5"] else -1
	
	@classmethod
	def mayores(cls, cuentas, fecha=None):	
		fecha = fecha if fecha else date.today()
		df = read_frame(cls.get_model('Operacion').objects.filter(
				cuenta__id__in=[cuentas.values_list('id', flat=True)], 
				# fecha__lte=fecha,
			).order_by('-fecha', '-id'), fieldnames=['fecha', 'documento', 'concepto', 'valor', 'detalle', 'documento__id', 'documento__receipt__receipt_type', 'cuenta__titulo__numero'])
		df['direccion'] = df['cuenta__titulo__numero'].apply(lambda x: 1 if str(x)[0] in ["1", "5"] else -1)
		df['fecha'] = pd.to_datetime(df['fecha'])
		df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
		df = df.rename(columns={'documento__receipt__receipt_type': 'receipt_type'})
		df['saldo'] = df['valor'][::-1].cumsum()
		df['debe'] = df['valor'].apply(lambda x: x if x > 0 else 0)
		df['haber'] = df['valor'].apply(lambda x: x if x < 0 else 0)
		df['monto'] = df['valor']*df['direccion']
		df['saldo'] = df['saldo']*df['direccion']
		return df	

	@classmethod
	def saldos(cls, cuentas, fecha=None):	
		fecha = fecha if fecha else date.today()
		df = read_frame(cls.get_model('Operacion').objects.filter(
				cuenta__id__in=[cuentas.values_list('id', flat=True)], 
				documento__isnull=False,
				documento__fecha_anulacion__isnull=True
			), fieldnames=['id', 'fecha', 'documento', 'concepto', 'fecha_indicativa','valor', 'documento__id', 'documento__receipt__receipt_type', 'vinculo__id', 'cuenta__titulo__numero'])
		df['direccion'] = df['cuenta__titulo__numero'].apply(lambda x: 1 if str(x)[0] in ["1", "5"] else -1)
		df['fecha'] = pd.to_datetime(df['fecha'])
		df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
		df['periodo'] = pd.to_datetime(df['fecha_indicativa'])
		df['periodo'] = df['periodo'].dt.strftime('%Y-%m')
		df = df.rename(columns={'documento__receipt__receipt_type': 'receipt_type'})
		
		pagos_capital = df.groupby('vinculo__id')['valor'].sum().reset_index()
		pagos_capital.columns = ['vinculo__id', 'valor']
		pagos_capital = pagos_capital.rename(columns={'vinculo__id': 'id', 'valor': 'pago_capital'})
		df = df.merge(pagos_capital, how='left', on='id')
		df = df[df['vinculo__id'].isna()]
		df['saldo'] = df['valor'] + df['pago_capital']
		df['saldo'] = df['saldo'].fillna(df['valor'])
		df = df[df['saldo']!=0]
		df['monto'] = df['valor']*df['direccion']
		df['pago_capital'] = df['pago_capital']*df['direccion']
		df['saldo'] = df['saldo']*df['direccion']
		return df




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
