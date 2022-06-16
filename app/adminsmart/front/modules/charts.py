import plotly.graph_objects as go
import pandas as pd

from django.db.models import Sum

from adminsmart.apps.core.models import Operacion


class BaseChart:

	TITLES = {
		'a_cobrar': "¿Cuánto queda por cobrar?",
		'arqueo': "¿Cuánto dinero hay disponible?",
		'a_pagar': "¿Cuánto falta pagar?"		
	}

	def __init__(self, handler='', *args, **kwargs):
		self.handler = handler
		self.title = self.TITLES[self.handler]
		self.id = self.ID
		self.kind = self.KIND

	def render(self):
		labels, values = getattr(self, self.handler)()
		fig = go.Figure(
			data=[self.FIGURE(labels=labels, values=values)],
			layout=go.Layout(
				margin=dict(l=50, r=50, t=0, b=0),
				legend=dict(orientation="h"),
			)
		)
		return fig.to_html()


class Pie(BaseChart):
	KIND = "donut"
	ID = 'donut_chart'
	FIGURE = go.Pie

	def a_cobrar(self):
		ops = Operacion.objects.filter(
			comunidad=self.comunidad,
			cuenta__naturaleza__nombre__in=["cliente", "dominio"],
		).values('fecha_indicativa', 'valor')
		df = pd.DataFrame.from_records(ops)
		df['fecha_indicativa'] = pd.to_datetime(df['fecha_indicativa']).dt.strftime('%Y-%m')
		df = df.groupby(['fecha_indicativa'])['valor'].sum().reset_index()
		df = df[df['valor'] > 0]
		return df['fecha_indicativa'].unique(), df['valor'].unique()

	def a_pagar(self):
		ops = Operacion.objects.filter(
			comunidad=self.comunidad,
			cuenta__naturaleza__nombre__in=["proveedor"],
		).values('fecha', 'valor')
		df = pd.DataFrame.from_records(ops)
		df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m')
		df = df.groupby(['fecha'])['valor'].sum().reset_index()
		df = df[df['valor'] > 0]
		return df['fecha'].unique(), df['valor'].unique()

	def arqueo(self):
		ops = Operacion.objects.filter(
			comunidad=self.comunidad,
			cuenta__naturaleza__nombre__in=["caja"],
		).values('cuenta__nombre', 'valor')
		df = pd.DataFrame.from_records(ops)
		df = df.groupby(['cuenta__nombre'])['valor'].sum().reset_index()
		df = df[df['valor'] > 0]
		return df['cuenta__nombre'].unique(), df['valor'].unique()

