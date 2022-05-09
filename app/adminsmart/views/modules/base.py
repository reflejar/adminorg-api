import hashlib
from django.views import generic
from django.core.cache import cache

from adminsmart.apps.core.models.cuenta import Cuenta

class BaseFrontView(generic.TemplateView):

	""" Base Front """
	
	paginate_by = 10

	def dispatch(self, request, *args, **kwargs):
		self.comunidad = self.request.user.perfil_set.first().comunidad
		return super(BaseFrontView, self).dispatch(request, *args, **kwargs)	

	def make_cache_key(self): return 'views_{}_{}'.format(self.MODULE_NATURALEZA, self.comunidad.id)

	def get_elements(self):
		elements = Cuenta.objects.filter(
			naturaleza__nombre=self.MODULE_NATURALEZA,
			comunidad=self.comunidad
		).values_list(
			'id', 'perfil__razon_social', 
			'perfil__apellido', 'perfil__nombre',
			'numero',  
		)
		return elements

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		key_cache = self.make_cache_key()
		
		elements = self.get_elements()
		# elements = cache.get(key_cache)
		if not elements:
			print("Hola")
			elements = self.get_elements()
			# hashed = hashlib.md5(str(result).encode())
			# cache.set(key_cache, hashed, 60*60*2)
			cache.set(key_cache, elements, 60*60*2)
			# elements = cache.get(key_cache)
		context.update({
			'module_name': self.MODULE_NAME,
			'comunidad': self.comunidad,
			'elements': elements
		})
		return context

class AdminFrontView(BaseFrontView):

	""" Base Admin Front """

	template_name = 'portals/admin.html'


class SocioFrontView(BaseFrontView):

	""" Base Socio Front """

	template_name = 'portals/socio.html'