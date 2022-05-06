from django.views import generic


class BaseFrontView(generic.TemplateView):

	""" Base Front """
	
	paginate_by = 10	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'module_name': self.MODULE_NAME,
			'comunidad': self.request.user.perfil_set.first().comunidad
		})
		return context

class AdminFrontView(BaseFrontView):

	""" Base Admin Front """

	template_name = 'portals/admin.html'


class SocioFrontView(BaseFrontView):

	""" Base Socio Front """

	template_name = 'portals/socio.html'

