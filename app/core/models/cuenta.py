from datetime import date
import pandas as pd
from django.db import models
from django.apps import apps
from django_pandas.io import read_frame

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
	domicilio = models.ForeignKey(Domicilio, blank=True, null=True, on_delete=models.PROTECT)
	numero = models.IntegerField(blank=True, null=True)
	nombre = models.CharField(max_length=150, blank=True, null=True)
	slug = models.CharField(max_length=150, blank=True, null=True)
	perfil = models.ForeignKey("users.Perfil", blank=True, null=True, on_delete=models.SET_NULL)
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

	@staticmethod
	def get_model(nombre):
		return apps.get_model('core', nombre)

	@property
	def direccion(self):
		return 1 if str(self.titulo.numero)[0] in ["1", "5"] else -1
	
	@classmethod
	def analisis(cls, cuentas, fecha=None):
		df = cls.mayores(cuentas, fecha)
		return df
	
	@classmethod
	def mayores(cls, cuentas, fecha=None):	
		fecha = fecha if fecha else date.today()
		df = read_frame(cls.get_model('Operacion').objects.filter(
				cuenta__id__in=[cuentas.values_list('id', flat=True)], 
				# fecha__lte=fecha,
			).order_by('-fecha', '-id'), fieldnames=['fecha', 'cuenta', 'documento', 'concepto', 'valor', 'detalle', 'documento__id', 'documento__receipt__receipt_type', 'cuenta__titulo__numero'])
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
		modulo = cuentas[0].naturaleza.nombre
		df = read_frame(cls.get_model('Operacion').objects.filter(
				cuenta__id__in=[cuentas.values_list('id', flat=True)], 
				documento__isnull=False,
				documento__fecha_anulacion__isnull=True
			), fieldnames=['id', 'fecha', 'documento', 'concepto', 'periodo','valor', 'detalle', 'documento__id', 'documento__receipt__receipt_type', 'vinculo__id', 'cuenta__titulo__numero', 'cuenta__naturaleza', 'fecha_vencimiento'])
		df['direccion'] = df['cuenta__titulo__numero'].apply(lambda x: 1 if str(x)[0] in ["1", "5"] else -1)
		df['fecha'] = pd.to_datetime(df['fecha'])
		df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
		df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'])
		df['fecha_vencimiento'] = df['fecha_vencimiento'].dt.strftime('%Y-%m-%d')		
		df['periodo'] = pd.to_datetime(df['periodo'])
		df['periodo'] = df['periodo'].dt.strftime('%Y-%m')
		df = df.rename(columns={'documento__receipt__receipt_type': 'receipt_type'})
		
		# Si es cliente o proveedor, el saldo se obtiene desde el vinculo.

		if modulo in ['cliente', 'proveedor']:
			pagos_capital = df.groupby('vinculo__id')['valor'].sum().reset_index()
			pagos_capital.columns = ['vinculo__id', 'valor']
			pagos_capital = pagos_capital.rename(columns={'vinculo__id': 'id', 'valor': 'pago_capital'})
			df = df.merge(pagos_capital, how='left', on='id')
			df = df[df['vinculo__id'].isna()]
		# Si es caja, el saldo se obtiene desde el detalle.
		else:
			df['detalle'] = df['detalle'].fillna("")
			df['pago_capital'] = df.groupby('detalle')['valor'].transform('sum')
			df = df.drop_duplicates(subset='detalle', keep='first')
			df['valor'] = 0


		df['saldo'] = df['valor'] + df['pago_capital']
		df['saldo'] = df['saldo'].fillna(df['valor'])
		df['monto'] = df['valor']*df['direccion']
		df = df[df['saldo']!=0]
		df['pago_capital'] = df['pago_capital']*df['direccion']
		df['saldo'] = df['saldo']*df['direccion']
		return df

