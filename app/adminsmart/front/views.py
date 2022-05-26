from io import BytesIO
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.http import (
	FileResponse,
	HttpResponseRedirect,
	Http404
)
from django.contrib.auth.decorators import login_required
from django.views import generic

from adminsmart.apps.utils.models import Comunidad
from adminsmart.apps.core.models import Documento

from .tools import (
	UserCommunityPermissions,
	UserObjectCommunityPermissions
)

DISPATCHER = {
	'superuser': settings.ADMIN_URL,
	'administrativo': settings.USER_ADMIN_LOGIN_REDIRECT,
	'socio': settings.USER_SOCIO_LOGIN_REDIRECT
}
	
@login_required
def index(request):
	group = "superuser" \
			if request.user.is_superuser \
			else request.user.groups.all()[0].name
	return HttpResponseRedirect(DISPATCHER[group])


class PDFViewer(
		UserCommunityPermissions, 
		UserObjectCommunityPermissions, 
		generic.DetailView
	):
	
	model = Documento

	def get(self, *args, **kwargs):
		""" Esto es necesario modificar para que los sirva sin guardarlo temporalmente"""
		documento = self.get_object()
		filename = str(documento)
		return FileResponse(documento.pdf.serve(), content_type='application/pdf', filename=f"{filename}.pdf")


class ChangeCommunity(generic.TemplateView, UserCommunityPermissions):
	
	""" Vista para cambiar de comunidad"""
	
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		profile = self.request.user.perfil_set.first()
		community = get_object_or_404(Comunidad.objects.all(), pk=request.POST["community"])
		if community in profile.comunidades.all():
			profile.comunidad = community
			profile.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))