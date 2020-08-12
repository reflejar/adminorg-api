from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import comunidades as comunidad_views



router = DefaultRouter()
router.register(r'comunidades', comunidad_views.ComunidadViewSet, base_name='comunidad')

urlpatterns = [
     path('', include(router.urls))
]