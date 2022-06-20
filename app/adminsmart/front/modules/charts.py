import plotly.graph_objects as go
import pandas as pd
import numpy as np

from django.db.models import Sum

from adminsmart.apps.core.models import Operacion


class Chart:

	KINDS = {
		'pie': go.Pie,
	}
	COLORS = ['#34d3eb','#ec6794','#32c861','#4489e4','#ffa91c','#5553ce','#f96a74']

	def __init__(
			self, 
			kind='pie', 
			title='',
			keep=[], 
			labels=[],  
			rank=None,
			*args, **kwargs
	):
		self.kind = self.KINDS[kind]
		self.keep = keep
		self.labels = labels
		self.title = title
		self.rank = rank

	def exec(self):
		labels = self.labels
		ops = Operacion.objects.filter(
			comunidad=self.comunidad,
			cuenta__naturaleza__nombre__in=self.keep,
		).values(self.labels, 'valor')
		df = pd.DataFrame.from_records(ops)
		if 'fecha' in self.labels:
			df[self.labels] = pd.to_datetime(df[self.labels  ]).dt.strftime('%Y-%m')
		df = df.groupby([self.labels])['valor'].sum().reset_index()
		df[self.labels] = df[self.labels].str.capitalize()
		df = df[df['valor'] > 0]
		if self.rank:
			df['ranked'] = df[self.labels].rank(ascending=False)\
				.apply(lambda x: np.nan if x <= self.rank else "Resto")\
				.fillna(df[self.labels])
			df = df.groupby(['ranked'])['valor'].sum().reset_index()
			labels = "ranked"
		return df[labels].tolist(), df['valor'].tolist()


	def render(self):
		labels, values = self.exec()
		fig = go.Figure(
			data=[self.kind(
				labels=labels, 
				text=labels, 
				textinfo="text+value", 
				values=values,
				marker=dict(colors=self.COLORS),
			)],
			layout=go.Layout(
				margin=dict(l=50, r=50, t=0, b=0),
				legend=dict(orientation="h"),
			)
		)
		return fig.to_html()


# class Pie(BaseChart):
# 	KIND = "donut"
# 	ID = 'donut_chart'
# 	FIGURE = go.Pie

# 	def a_pagar(self):
# 		ops = Operacion.objects.filter(
# 			comunidad=self.comunidad,
# 			cuenta__naturaleza__nombre__in=["proveedor"],
# 		).values('fecha', 'valor')
# 		df = pd.DataFrame.from_records(ops)
# 		df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m')
# 		df = df.groupby(['fecha'])['valor'].sum().reset_index()
# 		df = df[df['valor'] > 0]
# 		return df['fecha'].unique(), df['valor'].unique()

# 	def arqueo(self):
# 		ops = Operacion.objects.filter(
# 			comunidad=self.comunidad,
# 			cuenta__naturaleza__nombre__in=["caja"],
# 		).values('cuenta__nombre', 'valor')
# 		df = pd.DataFrame.from_records(ops)
# 		df = df.groupby(['cuenta__nombre'])['valor'].sum().reset_index()
# 		df = df[df['valor'] > 0]
# 		return df['cuenta__nombre'].unique(), df['valor'].unique()

