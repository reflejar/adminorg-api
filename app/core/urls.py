from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.parametros import ParametrosViewSet
from .views.estados import EstadosViewSet
from .views.comprobantes import ComprobantesViewSet

router = DefaultRouter()
router.register(r'parametros/(?P<naturaleza>[-a-zA-Z0-0_]+)', ParametrosViewSet, basename='operative')

router.register(r'comprobantes', ComprobantesViewSet, basename='operative')

router.register(r'estados/(?P<tipo>[-a-zA-Z0-0_]+)', EstadosViewSet, basename='operative')

urlpatterns = [
     path('', include(router.urls))
]