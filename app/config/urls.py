"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from .views import readiness, liveness


urlpatterns = [
	# Django Admin
	path(settings.ADMIN_URL, admin.site.urls),
	
	# K8s
	path('k8s/readiness/', readiness),
	path('k8s/liveness/', liveness),

	# Registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('recuperar-pass/', include('django.contrib.auth.urls')),
	path('signup/', LoginView.as_view(), name='signup'),
	
	# API
	path('users/', include(('adminsmart.users.urls', 'users'), namespace='users')),
	path('utils/', include(('adminsmart.utils.urls', 'utils'), namespace='utils')),
	path('files/', include(('adminsmart.files.urls', 'files'), namespace='files')),
	path('operative/', include(('adminsmart.core.urls', 'operative'), namespace='operative')),
	path('informes/', include(('adminsmart.informes.urls', 'informes'), namespace='informes')),
	path('api/', include(('adminsmart._public.urls', 'api'), namespace='api')),

	# Views
	path('', include(('adminsmart.views.urls', 'views'), namespace='views')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
