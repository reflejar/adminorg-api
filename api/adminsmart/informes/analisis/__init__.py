import json
from decimal import Decimal
import pandas as pd
import numpy as np

class Analisis:

	TRANSLATE = {
		'fecha': 'FECHA',
		'fecha_indicativa': 'PERIODO',
		'cuenta__naturaleza__nombre': 'NATURALEZA',
		'documento__receipt__receipt_type__description': 'DOCUMENTO_TIPO',
		'documento__receipt__receipt_number': 'DOCUMENTO_NUMERO',	
		'cuenta': 'CUENTA_ID',
		'cuenta__nombre': 'CUENTA_NOMBRE',
		'cuenta__titulo__nombre': 'TITULO_NOMBRE',
		'cuenta__titulo__numero': 'NUMERO',
		'descripcion': 'DESCRIPCION',
		'valor': 'VALOR',
		'cantidad': 'CANTIDAD',
		'vinculos__cuenta__nombre': 'CONCEPTO',
		'cuenta__perfil__nombre': 'CUENTA_PERFIL_NOMBRE',
		'cuenta__perfil__apellido': 'CUENTA_PERFIL_APELLIDO',
		}

	QUERY_TRANSLATE = {
		'concepto':'CONCEPTO', 
		'periodo':'PERIODO',
		'tipo_documento':'DOCUMENTO_TIPO',
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
		
		self.generate_initial_df(queryset.values(*self.TRANSLATE.keys()))
		
		
	def generate_initial_df(self, values):

		df = pd.DataFrame.from_records(values).copy()
		self.df = df.rename(columns = self.TRANSLATE)
		self.df['PERIODO'] = pd.to_datetime(self.df['PERIODO']).dt.strftime('%Y-%m')
		if 'titulo' in self.keep:
			self.df['NOMBRE'] = self.df['TITULO_NOMBRE']
			
		elif 'cliente' in self.keep or 'proveedor'  in self.keep:
			self.df['NOMBRE'] = self.df['CUENTA_PERFIL_APELLIDO'] + ", " + self.df['CUENTA_PERFIL_NOMBRE']
		else:
			self.df['NOMBRE'] = self.df['CUENTA_NOMBRE']


		if not 'titulo' in self.keep:
		 	self.df = self.df[self.df['NATURALEZA'].isin(self.keep)]

	def get_json(self):
		groups = ['NUMERO'] if 'titulo' in self.keep else []
		groups += ['NOMBRE'] + [self.QUERY_TRANSLATE[a] for a in self.group_by]
		
		columns = [self.QUERY_TRANSLATE[a] for a in self.column_by]
		
		if self.totalize == 'debe':
			debe_haber_df = self.df.copy()
			
			debe_haber_df['PERIODO'] = debe_haber_df.apply(lambda x: x['PERIODO'] + '/DEBE' if x['VALOR'] >= 0 else x['PERIODO'] + '/HABER', axis=1)
			debe_haber_df['VALOR'] = debe_haber_df['VALOR'].abs()
			self.df['PERIODO'] = self.df.apply(lambda x: x['PERIODO'] + "/SALDO", axis=1)
			
			self.df  = self.df.append(debe_haber_df)

		tabla_pivot = pd.pivot_table(
			data=self.df, 
			values=self.AGGREGATE_VALUES[self.totalize], 
			index=groups, 
			columns=columns, 
			aggfunc='sum'
		)
		tabla_pivot = tabla_pivot.dropna(axis=0, how='all').fillna(Decimal(0.00))
	
		if 'titulo' in self.keep:
			tabla_pivot = tabla_pivot.sort_values('NUMERO', ascending=True)
		else:
			tabla_pivot = tabla_pivot.sort_values('NOMBRE', ascending=True)
		
		return json.loads(tabla_pivot.reset_index().to_json(orient='records'))