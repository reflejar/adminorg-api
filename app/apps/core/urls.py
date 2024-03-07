from django.urls import include, path
from rest_framework.routers import DefaultRouter


from apps.core.views import (
     parametros,
     documentos,
     preconceptos,
     estados,
     importacion,
)

router = DefaultRouter()
router.register(r'parametros/(?P<naturaleza>[-a-zA-Z0-0_]+)', parametros.ParametrosViewSet, basename='operative')

router.register(r'documentos/cliente', documentos.ClienteViewSet, basename='operative')
router.register(r'documentos/proveedor', documentos.ProveedorViewSet, basename='operative')
router.register(r'documentos/tesoreria', documentos.TesoreriaViewSet, basename='operative')
router.register(r'documentos/asiento', documentos.AsientoViewSet, basename='operative')

router.register(r'preconceptos', preconceptos.PreConceptoViewSet, basename='operative')
router.register(r'importacion', importacion.ImportacionViewSet, basename='operative')

router.register(r'estados/(?P<tipo>[-a-zA-Z0-0_]+)', estados.EstadosViewSet, basename='operative')

urlpatterns = [
     path('', include(router.urls))
]