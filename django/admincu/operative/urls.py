from django.urls import include, path
from rest_framework.routers import DefaultRouter

from admincu.operative.views import (
     parametros,
     documentos,
     preconceptos,
     plataformas,
     estados
)

router = DefaultRouter()
router.register(r'parametros/(?P<naturaleza>[-a-zA-Z0-0_]+)', parametros.ParametrosViewSet, base_name='operative')

# router.register(r'documentos/cliente/(?P<code>[-a-zA-Z0-9_]+)', documentos.ClienteViewSet, base_name='operative')
router.register(r'documentos/cliente', documentos.ClienteViewSet, base_name='operative')
router.register(r'documentos/proveedor', documentos.ProveedorViewSet, base_name='operative')
router.register(r'documentos/tesoreria', documentos.TesoreriaViewSet, base_name='operative')
router.register(r'documentos/asiento', documentos.AsientoViewSet, base_name='operative')

router.register(r'preconceptos', preconceptos.PreConceptoViewSet, base_name='operative')

router.register(r'plataformas', plataformas.PlataformasViewSet, base_name='operative')
# router.register(r'plataformas/(?P<platform_code>[-a-zA-Z0-0_]+)', plataformas.PlataformasViewSet, base_name='operative')

router.register(r'estados/(?P<tipo>[-a-zA-Z0-0_]+)', estados.EstadosViewSet, base_name='operative')

urlpatterns = [
     path('', include(router.urls))
]