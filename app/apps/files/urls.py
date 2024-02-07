from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'carpetas', carpetas.CarpetaViewSet, basename='files')
router.register(r'archivos', archivos.ArchivoViewSet, basename='files')
router.register(r'pdf', pdfs.PDFViewSet, basename='files')

urlpatterns = [
     path('', include(router.urls))
]