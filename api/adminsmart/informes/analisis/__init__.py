import pandas as pd

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

		q = {'agrupar':self.group_by,'totalizar':self.totalize,'encolumnar':self.column_by}







		c = self.df.to_html()
		d = self.df.to_dict()

		return q, c, d