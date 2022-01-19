import pandas as pd
from datetime import datetime 
import numpy as np

class Analisis:
	
	def __init__(self, queryset, analisis_config):
		self.group_by = analisis_config['group_by']
		self.totalize = analisis_config['totalize']
		self.column_by = analisis_config['column_by']
		
		
		values = queryset.values(
			'fecha',
			'fecha_indicativa',	
			'valor',
			'descripcion',
			'cuenta',
			'cuenta__nombre',
			'cuenta__naturaleza__nombre',
			'cuenta__perfil__nombre',
			'cuenta__perfil__apellido',
			'cuenta__taxon__nombre',
			'cuenta__titulo__nombre',
			'documento__receipt__receipt_number',
			'documento__receipt__receipt_type__description',		
			'documento__descripcion')
		
		self.df = pd.DataFrame.from_records(values)
		
		

	def analisis(self):

		

		q = {'concepto':'cuenta', 'periodo':'mes_año','tipo_documento':'documento__receipt__receipt_type__description','valor':'sum','cantidad':'count','debe':'tipo_saldo','dia':'fecha'}


		if 'periodo' in self.column_by or 'periodo' in self.group_by:
			self.df = self.df.assign(mes_año=pd.to_datetime(self.df['fecha']))
			self.df['mes_año'] = self.df['mes_año'].dt.strftime('%Y-%m')
			

		if 'debe' in self.column_by or 'debe' in self.group_by:
			self.df['tipo_saldo'] = ["debe" if s >=0 else "haber" for s in self.df['valor']]
			self.df['valor'] = self.df['valor'].abs()


		encolumnar = []
		for a in self.column_by:
			encolumnar.append(q[a])

		agrupar = []
		for a in self.group_by:
			agrupar.append(q[a])


		tabla_pivot = self.df.pivot_table('valor',agrupar,encolumnar, aggfunc={'valor':q[self.totalize]})
		tabla_pivot = tabla_pivot.fillna(0)
		
		if 'debe' in self.column_by or 'debe' in self.group_by:
			tabla_pivot['saldo'] = np.cumsum(tabla_pivot['debe'] - tabla_pivot['haber']) 






		e = self.df.to_html()
		c = tabla_pivot.to_html()
		d = self.df.to_dict()
		f = str(tabla_pivot.to_dict())
		g = {'a': f}
		print(f)
		

		return q, e, c, g, d
		