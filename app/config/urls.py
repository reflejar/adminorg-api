"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from .views import ready


urlpatterns = [
	# Django Admin
	path(settings.ADMIN_URL, admin.site.urls),

	# K8s
	path('ready/', ready),
	
	# API
	path('', include(('apps.urls', 'api'), namespace="api")),

	# Views
	# ## Authentication
	# path('recuperar-pass/', include('django.contrib.auth.urls')),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
	# path('signup/', LoginView.as_view(), name='signup'),

	# ## Frontend
	# path('', include(('front.urls', 'views'), namespace='front')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
