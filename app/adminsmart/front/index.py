from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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