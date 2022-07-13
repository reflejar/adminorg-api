from django.views import generic
from apps.core.models import (
	Cuenta,
	Metodo,
	Titulo
)

from ..base import (
	BaseAdminView,
	AdminListObjectsView,
	AdminParametrosCUDView
)

from . import config



class IndexView(BaseAdminView):

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
			"bienes_de_cambio": Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="bien_de_cambio").count(),
			"intereses": Metodo.objects.filter(comunidad=self.comunidad, naturaleza="interes").count(),
			"descuentos": Metodo.objects.filter(comunidad=self.comunidad, naturaleza="descuento").count(),
			"titulos": Titulo.objects.filter(comunidad=self.comunidad).count(),
		})
		return context


class AddModuleContextData:

	@property
	def MODULE_BUTTONS(self): 
		module_buttons = config.MODULE_BUTTONS 
		if not 'contabilidad' in self.allowed_modules:
			module_buttons = list(filter(lambda button: not button['parameter'] in ['titulo'], module_buttons))
		if not 'stock' in self.allowed_modules:
			module_buttons = list(filter(lambda button: not button['parameter'] in ['bien_de_cambio'], module_buttons))
		if not 'cuentas-a-cobrar' in self.allowed_modules:
			module_buttons = list(filter(lambda button: not button['parameter'] in ['cliente', 'dominio', 'grupo', 'ingreso', 'interes', 'descuento'], module_buttons))			
		if not 'cuentas-a-pagar' in self.allowed_modules:
			module_buttons = list(filter(lambda button: not button['parameter'] in ['proveedor', 'gasto'], module_buttons))						
		return module_buttons

	@property
	def MODULE_HANDLER(self): return self.kwargs['naturaleza']
	
	@property
	def SUBMODULE(self): return {'name': self.kwargs['naturaleza']}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({"naturaleza": self.MODULE_HANDLER})
		return context	

class ListView(
		AddModuleContextData, 
		AdminListObjectsView
	):

	""" Vista de listado de cuentas, titulos y metodos """

	MODULE = config.MODULE
	template_name = f'{config.TEMPLATE_FOLDER}/list-objects.html'	


class CUParametroView(
		AddModuleContextData,
		AdminParametrosCUDView, 
		generic.CreateView,
		generic.UpdateView,
	):

	MODULE = config.MODULE
	template_name = f'{config.TEMPLATE_FOLDER}/cu-object.html'	


class DParametroView(
		AddModuleContextData,
		AdminParametrosCUDView, 
		generic.DeleteView,
	):

	MODULE = config.MODULE
	template_name = f'{config.TEMPLATE_FOLDER}/d-object.html'	