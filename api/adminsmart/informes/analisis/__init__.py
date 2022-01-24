import json
from decimal import Decimal
import pandas as pd

class OperacionAnalisis:

	COLUMN_NAMES = {
		'fecha': 'FECHA',
		'fecha_indicativa': 'PERIODO',
		'cuenta__naturaleza__nombre': 'NATURALEZA',
		'documento__receipt__receipt_type__description': 'DOCUMENTO_TIPO',
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
		'vinculos__cuenta__nombre': 'CONCEPTO',
		'descripcion': 'DESCRIPCION',
		'valor': 'VALOR',
		'cantidad': 'CANTIDAD',
		}

	QUERY_COLUMN_NAMES = {
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
		self.generate_initial_df(queryset.values(*self.COLUMN_NAMES.keys()))
		
		
	def generate_initial_df(self, values):

		df = pd.DataFrame.from_records(values).copy()
		self.df = df.rename(columns = self.COLUMN_NAMES)
		self.df['PERIODO'] = pd.to_datetime(self.df['PERIODO']).dt.strftime('%Y-%m')

		if 'titulo' in self.keep:
			self.df['NOMBRE'] = self.df['TITULO_NOMBRE']
		else:
			self.df['NOMBRE'] = self.df.apply(
					lambda x: x['PERFIL_RAZON_SOCIAL'] if x['PERFIL_RAZON_SOCIAL'] else ', '.join([x['PERFIL_APELLIDO'], x['PERFIL_NOMBRE']]) if x['NATURALEZA'] in ['cliente', 'proveedor']  \
					else '#' + str(int(x['CUENTA_NUMERO'])) if x['NATURALEZA'] in ['dominio'] \
					else x['CUENTA_NOMBRE'], 
					axis=1)

		if not 'titulo' in self.keep:
		 	self.df = self.df[self.df['NATURALEZA'].isin(self.keep)]

	def get_json(self):
		groups = ['TITULO_NUMERO'] if 'titulo' in self.keep else []
		groups += ['NOMBRE'] + [self.QUERY_COLUMN_NAMES[a] for a in self.group_by]

		columns = [self.QUERY_COLUMN_NAMES[a] for a in self.column_by]
		if self.totalize == 'debe':
			if len(columns) > 0:

				for c in columns:
					debe_haber_df = self.df.copy()
					debe_haber_df[c] = debe_haber_df.apply(lambda x: x[c] if x[c] != None else f'S/{c}', axis=1)
					debe_haber_df[c] = debe_haber_df.apply(lambda x: x[c] + '/DEBE' if x['VALOR'] >= 0 else x[c] + '/HABER', axis=1)
					debe_haber_df['VALOR'] = debe_haber_df['VALOR'].abs()

					self.df[c] = self.df.apply(lambda x: x[c] if x[c] != None else f'S/{c}', axis=1)
					self.df[c] = self.df.apply(lambda x: x[c] + "/SALDO", axis=1)
					
					self.df  = self.df.append(debe_haber_df)
			
			else:
				debe_haber_df = self.df.copy()
				debe_haber_df['TIPO_SALDO'] = debe_haber_df.apply(lambda x: 'DEBE' if x['VALOR'] >= 0 else 'HABER', axis=1)
				debe_haber_df['VALOR'] = debe_haber_df['VALOR'].abs()

				self.df['TIPO_SALDO'] = self.df.apply(lambda x: "SALDO", axis=1)

				self.df  = self.df.append(debe_haber_df)
				columns = ['TIPO_SALDO']

		tabla_pivot = pd.pivot_table(
			data=self.df, 
			values=self.AGGREGATE_VALUES[self.totalize], 
			index=groups, 
			columns=columns, 
			aggfunc='sum'
		)
		tabla_pivot = tabla_pivot.dropna(axis=0, how='all').fillna(Decimal(0.00))
	
		if 'titulo' in self.keep:
			tabla_pivot = tabla_pivot.sort_values('TITULO_NUMERO', ascending=True)
		else:
			tabla_pivot = tabla_pivot.sort_values('NOMBRE', ascending=True)
		
		return json.loads(tabla_pivot.reset_index().to_json(orient='records'))