import pandas as pd

class Analisis:
	
	def __init__(self, queryset, analisis_config):
		self.group_by = analisis_config['group_by']
		self.totalize = analisis_config['totalize']
		self.column_by = analisis_config['column_by']

	def analisis(queryset, analisis_config):
		q = queryset.values('cuenta')

		return q