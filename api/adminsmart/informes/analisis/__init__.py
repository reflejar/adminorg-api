import json
from decimal import Decimal
import pandas as pd

class OperacionAnalisis:

	COLUMN_NAMES = {
		'id': 'ID',
		'fecha': 'FECHA',
		'fecha_indicativa': 'PERIODO',
		'cuenta__naturaleza__nombre': 'NATURALEZA',
		'documento__receipt__receipt_type__description': 'TIPO_DOCUMENTO',
		'documento__receipt__receipt_number': 'DOCUMENTO_NUMERO',	
		'cuenta': 'CUENTA_ID',
		'cuenta__numero': 'CUENTA_NUMERO',
		'cuenta__nombre': 'CUENTA_NOMBRE',
		'cuenta__perfil__nombre': 'PERFIL_NOMBRE',
		'cuenta__perfil__apellido': 'PERFIL_APELLIDO',
		'cuenta__perfil__razon_social': 'PERFIL_RAZON_SOCIAL',
		'cuenta__titulo__nombre': 'TITULO_NOMBRE',
		'cuenta__titulo__numero': 'TITULO_NUMERO',
		'cuenta__vinculo1__id': 'CLIENTE_ID', # Solo para dominios
		'vinculo': 'VINCULO_ID',
		'descripcion': 'DESCRIPCION',
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
		self.generate_initial_df(queryset.values(*self.COLUMN_NAMES.keys()))
		
		
	def generate_initial_df(self, values):

		df = pd.DataFrame.from_records(values).copy()
		self.df = df.rename(columns = self.COLUMN_NAMES)
		self.df['PERIODO'] = pd.to_datetime(self.df['PERIODO']).dt.strftime('%Y-%m')
		self.df['VINCULO_ID'] = self.df['VINCULO_ID'].fillna(0).astype(int)

		if 'titulo' in self.keep:
			self.df['NOMBRE'] = self.df['TITULO_NOMBRE']
		else:
			self.df['NOMBRE'] = self.df.apply(
					lambda x: x['PERFIL_RAZON_SOCIAL'] if x['PERFIL_RAZON_SOCIAL'] else ', '.join([x['PERFIL_APELLIDO'], x['PERFIL_NOMBRE']]) if x['NATURALEZA'] in ['cliente', 'proveedor']  \
					else '#' + str(int(x['CUENTA_NUMERO'])) if x['NATURALEZA'] in ['dominio'] \
					else x['CUENTA_NOMBRE'], 
					axis=1)
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

		if not 'titulo' in self.keep:
		 	self.df = self.df[self.df['NATURALEZA'].isin(self.keep)]

		if 'debe' in self.totalize:
			self.df['TIPO_SALDO'] = ["DEBE" if s >=0 else "HABER" for s in self.df['VALOR']]
			df_temp = self.df.copy()
			df_temp['TIPO_SALDO'] = "SALDO"
			self.df['VALOR'] = self.df['VALOR'].abs()
			self.df = self.df.append(df_temp)

		
	def generate_groups(self):
		groups = ['TITULO_NUMERO'] if 'titulo' in self.keep else []
		groups += ['NOMBRE'] + [a.upper() for a in self.group_by]		
		return groups

	def generate_columns(self):
		columns = [a.upper() for a in self.column_by]
		if self.totalize == 'debe':
			columns.append('TIPO_SALDO')
		return columns		

	def sort_pivot_df(self):
		if 'titulo' in self.keep:
			self.pivot_df = self.pivot_df.sort_values('TITULO_NUMERO', ascending=True)
		else:
			self.pivot_df = self.pivot_df.sort_values('NOMBRE', ascending=True)

	def get_json(self):
		
		groups = self.generate_groups()
		columns = self.generate_columns()

		self.pivot_df = pd.pivot_table(
			data=self.df, 
			values=self.AGGREGATE_VALUES[self.totalize], 
			index=groups, 
			columns=columns, 
			aggfunc='sum'
		)
		self.pivot_df = self.pivot_df.dropna(axis=0, how='all').fillna(Decimal(0.00))	
	
		self.sort_pivot_df()
		
		return json.loads(self.pivot_df.reset_index().to_json(orient='split'))
