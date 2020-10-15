"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('users/', include(('admincu.users.urls', 'users'), namespace='users')),
    path('utils/', include(('admincu.utils.urls', 'utils'), namespace='utils')),
    path('files/', include(('admincu.files.urls', 'files'), namespace='files')),
    path('operative/', include(('admincu.operative.urls', 'operative'), namespace='operative')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
