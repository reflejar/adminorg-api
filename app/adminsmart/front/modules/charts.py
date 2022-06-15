from decimal import Decimal
from django.db.models import Sum

from adminsmart.apps.core.models import Operacion


class BaseChart:

	def __init__(self, handler='', *args, **kwargs):
		self.handler = handler
		self.title = self.TITLES[self.handler]
		self.id = self.ID
		self.kind = self.KIND

	def values(self):
		return getattr(self, self.handler)()		

class Donut(BaseChart):
	KIND = "donut"
	ID = 'donut_chart'
	TITLES = {
		'a_cobrar': "¿Cuánto queda por cobrar?",
		'arqueo': "¿Cuánto dinero hay disponible?"
	}

	def a_cobrar(self):
		return [
		{
			'name': 'Facturado',
			'value': Operacion.objects.filter(
				comunidad=self.comunidad,
				cuenta__naturaleza__nombre__in=["cliente", "dominio"],
				valor__gte=0,
			).aggregate(Sum('valor'))['valor__sum']
		},
		{
			'name': 'Adeudado',
			'value': Operacion.objects.filter(
				comunidad=self.comunidad,
				cuenta__naturaleza__nombre__in=["cliente", "dominio"],
			).aggregate(Sum('valor'))['valor__sum']
		}
		]		



class Gauge(BaseChart):

	KIND = "gauge"
	ID = "gauge_chart"
	TITLES = {
		'a_cobrar': "¿Cuánto falta cobrar?",
		'a_pagar': "¿Cuánto falta pagar?"
	}

	def a_cobrar(self):
		return [
		{
			'name': 'Facturado',
			'value': Operacion.objects.filter(
				comunidad=self.comunidad,
				cuenta__naturaleza__nombre__in=["cliente", "dominio"],
				valor__gte=0,
			).aggregate(Sum('valor'))['valor__sum']
		},
		{
			'name': 'Adeudado',
			'value': Operacion.objects.filter(
				comunidad=self.comunidad,
				cuenta__naturaleza__nombre__in=["cliente", "dominio"],
			).aggregate(Sum('valor'))['valor__sum']
		}
		]		

	def a_pagar(self):
		return [
				{
					'name': 'Comprado',
					'value': Operacion.objects.filter(
						comunidad=self.comunidad,
						cuenta__naturaleza__nombre__in=["proveedor"],
						valor__lte=0,
					).aggregate(Sum('valor'))['valor__sum']
				},
				{
					'name': 'Deudas',
					'value': Operacion.objects.filter(
						comunidad=self.comunidad,
						cuenta__naturaleza__nombre__in=["proveedor"],
					).aggregate(Sum('valor'))['valor__sum']
				}
			]		

	def gauge(self):
		values = self.values()
		return int(values[1]['value'] / values[0]['value'])