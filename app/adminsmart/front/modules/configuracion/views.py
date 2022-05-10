from django.db.models import F

from adminsmart.apps.core.models import (
	Cuenta,
	Metodo,
	Titulo
)

from ..base import AdminFrontView

from .buttons import MODULE_BUTTONS

class IndexView(AdminFrontView):

	""" Vista de configuracion """

	MODULE_NAME = "Configuracion"
	MODULE_NATURALEZA = ""
	template_name = 'configuracion/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			"clientes": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="cliente").count(),
			"dominios": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="dominio").count(),
			"proveedores": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="proveedor").count(),
			"grupos": 0,
			"cajas": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="caja").count(),
			"ingresos": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="ingreso").count(),
			"gastos": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="gasto").count(),
			"intereses": Metodo.objects.filter(comunidad=self.comunidad, naturaleza="interes").count(),
			"descuentos": Metodo.objects.filter(comunidad=self.comunidad, naturaleza="descuento").count(),
			"titulos": Titulo.objects.filter(comunidad=self.comunidad).count(),
		})
		return context


class ListView(IndexView):

	""" Vista de listado de cuentas, titulos y metodos """

	MODULE_NAME = "Configuracion"
	template_name = 'configuracion/list.html'
	MODULE_BUTTONS = MODULE_BUTTONS

	def get_objects(self):
		if self.kwargs['naturaleza'] == "titulo":
			return Titulo.objects.filter(comunidad=self.comunidad)\
				.order_by("numero")\
				.annotate(predeterminado_para=F('predeterminado__nombre'))\
				.values(
				'numero','nombre',
				'predeterminado_para'
				)
		if not self.kwargs['naturaleza'] in ['titulo', 'interes', 'descuento']:
			if self.kwargs['naturaleza'] in ['ingreso', 'gasto']:
				return Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.kwargs['naturaleza'])\
					.order_by("nombre")\
					.annotate(
						titulo_contable=F('titulo__nombre'),
					)\
					.values(
						'nombre', 'titulo_contable'
					)
			elif self.kwargs['naturaleza'] == "caja":
				return Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.kwargs['naturaleza'])\
					.order_by("nombre")\
					.annotate(
						tipo=F('taxon__nombre'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						'nombre', 'tipo', 'titulo_contable'
					)
		else:
			return Metodo.objects.filter(comunidad=self.comunidad, naturaleza=self.kwargs['naturaleza'])\
				.order_by('-id')\
				.values(
				"nombre","tipo",
				"plazo","monto",
				)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		objects = self.get_objects()
		context.update({
			"naturaleza": kwargs['naturaleza'],
			"objects": objects,
			"titles": objects.first().keys() if objects else []
		})
		return context

	