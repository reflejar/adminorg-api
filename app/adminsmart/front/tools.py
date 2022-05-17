from django.shortcuts import get_object_or_404 
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import (
	Http404,
	HttpResponseRedirect
)

class UserCommunityPermissions(LoginRequiredMixin):

	def dispatch(self, request, *args, **kwargs):
		try:
			self.comunidad = self.request.user.perfil_set.first().comunidad
		except:
			return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
		
		return super().dispatch(request, *args, **kwargs)


class UserObjectCommunityPermissions:

	def get_object(self, queryset=None, *args, **kwargs):
		self.object = super().get_object(queryset, *args, **kwargs)
		if self.object.comunidad != self.comunidad:
			raise Http404("No se encontró el objeto")
		return self.object