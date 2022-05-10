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
	
	# API
	path('api/', include(('adminsmart.api.urls', 'api'), namespace="api")),

	# Views
	## Authentication
	path('recuperar-pass/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('signup/', LoginView.as_view(), name='signup'),

	## Frontend
	path('', include(('adminsmart.front.urls', 'views'), namespace='front')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
