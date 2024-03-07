from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.parametros import ParametrosViewSet
from .views.estados import EstadosViewSet
from .views.comprobantes import ComprobantesViewSet
# from apps.core.views import (
#      documentos,
#      preconceptos,
#      estados,
#      importacion,
# )

router = DefaultRouter()
router.register(r'parametros/(?P<naturaleza>[-a-zA-Z0-0_]+)', ParametrosViewSet, basename='operative')

router.register(r'comprobantes/(?P<naturaleza>[-a-zA-Z0-0_]+)', ComprobantesViewSet, basename='operative')
# router.register(r'documentos/proveedor', documentos.ProveedorViewSet, basename='operative')
# router.register(r'documentos/tesoreria', documentos.TesoreriaViewSet, basename='operative')
# router.register(r'documentos/asiento', documentos.AsientoViewSet, basename='operative')

# router.register(r'preconceptos', preconceptos.PreConceptoViewSet, basename='operative')
# router.register(r'importacion', importacion.ImportacionViewSet, basename='operative')

router.register(r'estados/(?P<tipo>[-a-zA-Z0-0_]+)', EstadosViewSet, basename='operative')

urlpatterns = [
     path('', include(router.urls))
]