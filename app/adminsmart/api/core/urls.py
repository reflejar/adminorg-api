from django.urls import include, path
from rest_framework.routers import DefaultRouter


from adminsmart.api.core.views import (
     parametros,
     documentos,
     preconceptos,
     # plataformas,
     estados,
     informes,
     importacion,
)

router = DefaultRouter()
router.register(r'parametros/(?P<naturaleza>[-a-zA-Z0-0_]+)', parametros.ParametrosViewSet, basename='operative')

# router.register(r'documentos/cliente/(?P<code>[-a-zA-Z0-9_]+)', documentos.ClienteViewSet, basename='operative')
router.register(r'documentos/cliente', documentos.ClienteViewSet, basename='operative')
router.register(r'documentos/proveedor', documentos.ProveedorViewSet, basename='operative')
router.register(r'documentos/tesoreria', documentos.TesoreriaViewSet, basename='operative')
router.register(r'documentos/asiento', documentos.AsientoViewSet, basename='operative')

router.register(r'preconceptos', preconceptos.PreConceptoViewSet, basename='operative')
router.register(r'importacion', importacion.ImportacionViewSet, basename='operative')

# router.register(r'plataformas', plataformas.PlataformasViewSet, basename='operative')
# router.register(r'plataformas/(?P<platform_code>[-a-zA-Z0-0_]+)', plataformas.PlataformasViewSet, basename='operative')

router.register(r'estados/(?P<tipo>[-a-zA-Z0-0_]+)', estados.EstadosViewSet, basename='operative')

router.register(r'informes', informes.InformesViewSet, basename='operative')

urlpatterns = [
     path('', include(router.urls))
]