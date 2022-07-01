from decimal import Decimal
import numpy as np
import pandas as pd
from .models import (
	Cuenta,
	Operacion
)

class Report:

	COLUMN_NAMES = {
		'id': 'ID',
		'fecha': 'FECHA',
		'fecha_indicativa': 'PERIODO',
		'cuenta__naturaleza__nombre': 'NATURALEZA',
		'documento__receipt__receipt_type__description': 'TIPO_DOCUMENTO',
		'documento__receipt__point_of_sales': 'DOCUMENTO_PUNTO',	
		'documento__receipt__receipt_number': 'DOCUMENTO_NUMERO',	
		'cuenta': 'CUENTA_ID',
		'cuenta__numero': 'CUENTA_NUMERO',
		'cuenta__nombre': 'CUENTA_NOMBRE',
		'cuenta__perfil__nombre': 'PERFIL_NOMBRE',
		'cuenta__perfil__apellido': 'PERFIL_APELLIDO',
		'cuenta__perfil__razon_social': 'PERFIL_RAZON_SOCIAL',
		'cuenta__titulo__nombre': 'TITULO_NOMBRE',
		'cuenta__titulo__numero': 'TITULO_NUMERO',
		'vinculo': 'VINCULO_ID',
		'documento__destinatario': "COMPROBANTE_DESTINATARIO_ID",
		'detalle': 'DETALLE',
		'documento__descripcion': 'DESCRIPCION',
		'valor': 'VALOR',
		'cantidad': 'CANTIDAD',
		}

	AGGREGATE_VALUES = {
		'valor':'VALOR',
		'debe': 'VALOR',
		'cantidad': 'CANTIDAD'
	}		

	def __init__(
			self, 
			comunidad,
			data=None,
			keep=[]
		):
		self.comunidad = comunidad
		self.keep = keep
		self.labels = pd.DataFrame.from_records([
			{
				'CUENTA_ID': c.id, 
				'NATURALEZA': c.naturaleza.nombre,
				'NOMBRE': str(c) if c.naturaleza.nombre != "dominio" else str(c.inquilino())
			} for c in Cuenta.objects.filter(
					comunidad=comunidad, 
					).select_related(
						"naturaleza",
					).prefetch_related(
						"vinculo2",
					)
		])
		if data:
			self.df = self.generate_initial_df(data.values(*self.COLUMN_NAMES.keys()))
		else:
			self.df = self.generate_initial_df(Operacion.objects.filter(comunidad=self.comunidad).select_related(
					"cuenta", 
					"cuenta__perfil", # Para el nombre de la cuenta
					"cuenta__titulo", 
					"cuenta__naturaleza",
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
				))
		


	def prepare_cuenta_vinculada(self):
		self.labels['COMPROBANTE_DESTINATARIO_ID'] = self.labels['CUENTA_ID']
		self.labels['CUENTA_VINCULADA'] = self.labels['NOMBRE']
		self.labels = self.labels[["COMPROBANTE_DESTINATARIO_ID", 'CUENTA_VINCULADA']]
		self.df['COMPROBANTE_DESTINATARIO_ID'] = self.df['COMPROBANTE_DESTINATARIO_ID'].fillna(0)
		self.df = pd.merge(self.df, self.labels, on=['COMPROBANTE_DESTINATARIO_ID'])


	def generate_initial_df(self, values):

		df = pd.DataFrame.from_records(values).copy()
		if len(df):
			df = df.rename(columns = self.COLUMN_NAMES)
			# Preparacion del periodo
			df['PERIODO'] = pd.to_datetime(df['PERIODO']).dt.strftime('%Y-%m')
			# Preparacion del vinculo
			df['VINCULO_ID'] = df['VINCULO_ID'].fillna(0).astype(int)

			# Preparacion de los nombres
			if 'titulo' in self.keep:
				df['NOMBRE'] = df['TITULO_NOMBRE']
			else:
				df = pd.merge(df, self.labels, on=['CUENTA_ID', 'NATURALEZA'])
			
			# Preparacion del dominio
			if 'cliente' in self.keep:
				df['DOMINIO'] = df['CUENTA_NUMERO'].fillna(0).astype(int).astype(str).replace("0","-")
			
			# Mantener los solicitados
			if self.keep and not 'titulo' in self.keep:
				if 'cliente' in self.keep:
					self.keep.append("dominio")
				df = df[df['NATURALEZA'].isin(self.keep)]

		df = df.drop_duplicates()
		return df
		
	def generate_groups(self, group_by):
		groups = ['TITULO_NUMERO'] if 'titulo' in self.keep else []
		groups += ['NOMBRE'] 
		if 'cliente' in self.keep:
			groups.append("DOMINIO")
		groups += [a.upper() for a in group_by]
		return groups

	def generate_columns(self, columns, totalize):
		columns = [a.upper() for a in columns]
		if totalize == 'debe':
			columns.append('TIPO_SALDO')
		return columns		

	def sort_rows_pivot_df(self):
		if 'titulo' in self.keep:
			self.pivot_df = self.pivot_df.sort_values('TITULO_NUMERO', ascending=True)
		elif set(['ingreso', 'gasto']).issubset(self.keep):
			self.pivot_df = self.pivot_df.sort_values('NOMBRE', ascending=True)

	def sort_columns_pivot_df(self, columns):
		if len(columns) > 0:
			col = columns[0]
			ordered = self.df[col].sort_values(ascending=False if col == "PERIODO" else True).unique()
			if len(columns) > 1:
				self.pivot_df = self.pivot_df.reindex(columns=ordered, level=col)
			else:
				if not 'TIPO_SALDO' in columns:
					ordered = ['TOTAL'] + list(ordered)
				self.pivot_df = self.pivot_df.reindex(ordered, axis=1)

	def generate_pivot_table(self, groups, columns):
		self.pivot_df = pd.pivot_table(
			data=self.df, 
			values=self.AGGREGATE_VALUES[self.totalize], 
			index=groups, 
			columns=columns, 
			aggfunc='sum'
		)
		self.pivot_df = self.pivot_df\
			.replace(Decimal(0), np.nan)\
			.replace(Decimal(0.00), np.nan)\
			.fillna(Decimal(0.00))
		
		if len(self.column_by) != 0 and 'valor' in self.totalize:
			self.pivot_df['TOTAL'] = self.pivot_df.sum(axis=1)
			self.pivot_df = self.pivot_df[self.pivot_df['TOTAL'] != Decimal(0.00)]

	def prepare_dhs(self):
		df_temp = self.df.copy()
		df_temp['TIPO_SALDO'] = "SALDO"
		self.df['TIPO_SALDO'] = ["DEBE" if s >=0 else "HABER" for s in self.df['VALOR']]
		self.df['VALOR'] = self.df['VALOR'].abs()
		self.df = self.df.append(df_temp)

	def prepare_conceptos(self):
		# Generacion del concepto
		df_conceptos = self.df.copy()
		
		df_conceptos = df_conceptos[df_conceptos['NATURALEZA'].isin(
				['ingreso']
			)][['NOMBRE', 'VINCULO_ID']].rename(
				columns={'NOMBRE': 'CONCEPTO_PADRE', 'VINCULO_ID': 'VINCULO_ID_PADRE'}
			)
		df_conceptos = df_conceptos[df_conceptos['VINCULO_ID_PADRE'] != 0]

		df_a_conceptuar = self.df.copy()
		df_a_conceptuar= df_a_conceptuar[df_a_conceptuar['NATURALEZA'].isin(
			['cliente', 'dominio', 'proveedor']
		)][['ID', 'VINCULO_ID']]
		df_a_conceptuar['VINCULO_ID_PADRE'] = df_a_conceptuar['ID']

		df_a_conceptuar = pd.merge(df_a_conceptuar,df_conceptos, on='VINCULO_ID_PADRE', how='left')

		df_conceptos_hijo = df_conceptos.rename(
				columns={'CONCEPTO_PADRE': 'CONCEPTO_HIJO', 'VINCULO_ID_PADRE':'VINCULO_ID_HIJO'}
			)
		df_conceptos_hijo = df_conceptos_hijo[df_conceptos_hijo['VINCULO_ID_HIJO'] != 0]

		df_a_conceptuar = df_a_conceptuar.rename(
			columns={'VINCULO_ID': 'VINCULO_ID_HIJO'}
		)
		df_a_conceptuar = pd.merge(df_a_conceptuar, df_conceptos_hijo, on='VINCULO_ID_HIJO', how='left')
		self.df = pd.merge(self.df, df_a_conceptuar, on='ID', how='left')

		self.df['CONCEPTO'] = self.df['CONCEPTO_PADRE'].fillna(self.df['CONCEPTO_HIJO'])
		self.df['CONCEPTO'] = self.df['CONCEPTO'].fillna("")		

	def get_df(
		self, 
		group_by=[],
		columns=[],
		totalize="valor"	,	
		raw_data=False
	):

		if 'concepto' in group_by + columns or len(self.keep) == 0:
			self.prepare_conceptos()

		# self.prepare_cuenta_vinculada()

		if 'debe' in totalize:
			self.prepare_dhs()

		if not len(self.df) or (not raw_data and not self.keep):
			return pd.DataFrame()
		if raw_data:
			return self.df

		groups = self.generate_groups(group_by)
		columns = self.generate_columns(columns)

		self.generate_pivot_table(groups, columns)
		self.sort_rows_pivot_df()
		self.sort_columns_pivot_df(columns)
		return self.pivot_df.reset_index()