from django.urls import include, path

from .views import *

urlpatterns = [

	# Custom Views
	path('', IndexView.as_view(), name='index'),
	path('<int:pk>/deudas', EstadoDeudasView.as_view(), name='deudas'),
	path('<int:pk>/cuenta', EstadoCuentaView.as_view(), name='cuenta'),

]


