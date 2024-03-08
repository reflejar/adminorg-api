import json
from decimal import Decimal
import numpy as np
import pandas as pd
from django_pandas.io import read_frame

class OperacionAnalisis:

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
		'concepto__nombre': 'CONCEPTO',
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

	def __init__(self, queryset, analisis_config):
		self.keep = analisis_config['analizar']
		self.group_by = analisis_config['agrupar_por']
		self.column_by = analisis_config['encolumnar']
		self.totalize = analisis_config['totalizar']
		self.generate_initial_df(read_frame(queryset, fieldnames=list(self.COLUMN_NAMES.keys())))
		

	def filter_query(self):
		if self.keep and not 'titulo' in self.keep:
			if 'cliente' in self.keep:
				self.keep.append("dominio")
			self.df = self.df[self.df['NATURALEZA'].isin(self.keep)]		

	def prepare_dhs(self):
		df_temp = self.df.copy()
		df_temp['TIPO_SALDO'] = "SALDO"
		self.df['TIPO_SALDO'] = ["DEBE" if s >=0 else "HABER" for s in self.df['VALOR']]
		self.df['VALOR'] = self.df['VALOR'].abs()
		self.df = self.df.append(df_temp)

	def generate_initial_df(self, dataframe):

		df = dataframe
		if len(df):
			self.df = df.rename(columns = self.COLUMN_NAMES)
			self.df['PERIODO'] = pd.to_datetime(self.df['PERIODO']).dt.strftime('%Y-%m')
			self.df['VINCULO_ID'] = self.df['VINCULO_ID'].fillna(0).astype(int)
			self.df['NOMBRE'] = self.df['TITULO_NOMBRE' if 'titulo' in self.keep else 'CUENTA_NOMBRE']

			self.filter_query()

			if 'debe' in self.totalize:
				self.prepare_dhs()
		else:
			self.df = df

		self.df = self.df.drop_duplicates()						
		
	def generate_groups(self):
		groups = ['TITULO_NUMERO'] if 'titulo' in self.keep else []
		groups += ['NOMBRE'] 
		groups += [a.upper() for a in self.group_by]
		
		return groups

	def generate_columns(self):
		columns = [a.upper() for a in self.column_by]
		if self.totalize == 'debe':
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


	def get_df(self, raw_data=False):
		if not len(self.df) or (not raw_data and not self.keep):
			return pd.DataFrame()
		if raw_data:
			return self.df

		return self.df
		groups = self.generate_groups()
		columns = self.generate_columns()
		self.generate_pivot_table(groups, columns)
		self.sort_rows_pivot_df()
		self.sort_columns_pivot_df(columns)
		return self.pivot_df.reset_index()
