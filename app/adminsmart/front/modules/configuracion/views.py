from adminsmart.apps.core.models import (
	Cuenta,
	Metodo,
	Titulo
)

from ..base import AdminListObjectsView

from . import config



class IndexView(AdminListObjectsView):

	""" Vista de configuracion """

	MODULE = config.MODULE
	MODULE_HANDLER = ""
	template_name = f'{config.TEMPLATE_FOLDER}/index.html'

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


class ListView(AdminListObjectsView):

	""" Vista de listado de cuentas, titulos y metodos """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	template_name = 'configuracion/list-objects.html'	

	def get_context_data(self, **kwargs):
		self.MODULE_HANDLER = kwargs['naturaleza']
		self.SUBMODULE = {'name': kwargs['naturaleza']}
		context = super().get_context_data(**kwargs)
		context.update({"naturaleza": self.MODULE_HANDLER})
		return context

	