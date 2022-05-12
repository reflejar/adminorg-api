from itertools import groupby
from django.db.models import F
import hashlib
from django.views import generic
from django.core.cache import cache

from adminsmart.apps.core.models import (
	Cuenta,
	Metodo,
	Titulo
)

class BaseFrontView(generic.TemplateView):

	""" Base Front """
	
	template_name = 'layout.html'
	paginate_by = 10

	def dispatch(self, request, *args, **kwargs):
		self.comunidad = self.request.user.perfil_set.first().comunidad
		return super(BaseFrontView, self).dispatch(request, *args, **kwargs)	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'comunidad': self.comunidad,
			'module_name': self.MODULE_NAME,
		})
		return context

class AdminFrontView(BaseFrontView):

	""" Base Admin Front """

	def make_cache_key(self): return f'views_{self.MODULE_NATURALEZA}_{self.comunidad.id}'

	def get_all_itulo(self):
		return list(Titulo.objects.filter(comunidad=self.comunidad)\
			.order_by("numero")\
			.annotate(predeterminado_para=F('predeterminado__nombre'))\
			.values(
			'id', 'numero','nombre',
			'predeterminado_para'
			))
		
	def get_all_caja(self): 
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_NATURALEZA)\
					.order_by("nombre")\
					.annotate(
						tipo=F('taxon__nombre'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						'id', 'nombre', 'tipo', 'titulo_contable'
					))		
	get_all_gasto = get_all_caja	

	def get_all_ingreso(self):
		cuentas = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_NATURALEZA)\
			.order_by("nombre")\
			.annotate(
				metodos_descuento_interes=F('metodos__nombre'),
				titulo_contable=F('titulo__nombre'),
			)\
			.values(
				'id', 'nombre', 'metodos_descuento_interes', 'titulo_contable'
			)				
		
		objects = []
		for _, value in groupby(cuentas, lambda x: x['nombre']):
			parsed_object = list(value)
			primary_object = parsed_object[0].copy()
			if len(parsed_object) > 1:
				primary_object['metodos_descuento_interes'] = ", ".join(o["metodos_descuento_interes"] for o in parsed_object)
			objects.append(primary_object)
		return objects		

	def get_all_interes(self):
		return list(Metodo.objects.filter(comunidad=self.comunidad, naturaleza=self.MODULE_NATURALEZA)\
				.order_by('-id')\
				.values(
				'id',"nombre","tipo",
				"plazo","monto",
				))
	get_all_descuento = get_all_interes	

	def get_all_cliente(self): 
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_NATURALEZA)\
					.order_by("perfil__apellido")\
					.annotate(
						apellido_cliente=F('perfil__apellido'),
						nombre_cliente=F('perfil__nombre'),
						razon_social=F('perfil__razon_social'),
						tipo_documento=F('perfil__tipo_documento__description'),
						documento=F('perfil__numero_documento'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						'id', 'apellido_cliente','nombre_cliente','razon_social',
						'tipo_documento','documento','titulo_contable',
					))		

	def get_all_proveedor(self): 
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_NATURALEZA)\
					.annotate(
						razon_social=F('perfil__razon_social'),
						apellido_proveedor=F('perfil__apellido'),
						nombre_proveedor=F('perfil__nombre'),
						tipo_documento=F('perfil__tipo_documento__description'),
						documento=F('perfil__numero_documento'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						'id', 'razon_social','apellido_proveedor','nombre_proveedor',
						'tipo_documento','documento','titulo_contable',
					))		

	def get_all_dominio(self): 
		cuentas = list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_NATURALEZA)\
					.order_by('numero')\
					.values(
						'id', 'numero', 
						'vinculo2__cuenta__perfil__apellido','vinculo2__cuenta__perfil__nombre', 
						'vinculo2__definicion__nombre'
					))	
		objects = []
		for _, value in groupby(cuentas, lambda x: x['numero']):
			parsed_object = list(value)
			primary_object = parsed_object[0].copy()
			primary_object['relaciones'] = ", ".join(
				f'{o["vinculo2__definicion__nombre"]}: {o["vinculo2__cuenta__perfil__apellido"]}, {o["vinculo2__cuenta__perfil__nombre"]}' for o in parsed_object
			)
			objects.append(primary_object)
			primary_object.pop("vinculo2__definicion__nombre")
			primary_object.pop("vinculo2__cuenta__perfil__apellido")
			primary_object.pop("vinculo2__cuenta__perfil__nombre")
		return objects						

	def get_all_grupo(self): return []

	def get_objects(self): # Funcion pensada para cachear
		method = getattr(self, f"get_all_{self.MODULE_NATURALEZA}")
		objects = method()
		return objects	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if getattr(self, "MODULE_BUTTONS", False):
			context.update({'sidebuttons': self.MODULE_BUTTONS})
		if getattr(self, "MODULE_NATURALEZA", False):
			objects = self.get_objects()
			context.update({
				"objects": objects,
				"titles": objects[0].keys() if objects else []
			})
		return context


class SocioFrontView(BaseFrontView):

	""" Base Socio Front """
