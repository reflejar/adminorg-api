from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InformesViewSet

router = DefaultRouter()

router.register(r'', InformesViewSet, basename='reportes')

urlpatterns = [
     path('', include(router.urls))
]