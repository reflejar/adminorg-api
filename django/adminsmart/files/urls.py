from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'carpetas', carpetas.CarpetaViewSet, base_name='files')
router.register(r'archivos', archivos.ArchivoViewSet, base_name='files')
router.register(r'pdf', pdfs.PDFViewSet, base_name='files')

urlpatterns = [
     path('', include(router.urls))
]