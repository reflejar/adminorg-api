"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('users/', include(('adminsmart.users.urls', 'users'), namespace='users')),
    path('utils/', include(('adminsmart.utils.urls', 'utils'), namespace='utils')),
    path('files/', include(('adminsmart.files.urls', 'files'), namespace='files')),
    path('operative/', include(('adminsmart.operative.urls', 'operative'), namespace='operative')),
    path('informes/', include(('adminsmart.informes.urls', 'informes'), namespace='informes')),
    path('api/', include(('adminsmart._public.urls', 'api'), namespace='api')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
