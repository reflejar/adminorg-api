from io import BytesIO
from django.http import FileResponse

from django.conf import settings
from django.http import (
	FileResponse,
	HttpResponseRedirect
)
from django.contrib.auth.decorators import login_required
from django.views import generic

from adminsmart.apps.core.models import Documento
from .tools import UserCommunityPermissions, UserObjectCommunityPermissions

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