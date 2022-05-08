from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import users as user_view


router= DefaultRouter()
router.register(r'', user_view.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]