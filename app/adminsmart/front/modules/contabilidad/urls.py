from django.urls import path

from ..base import BlankView

from .views import *

urlpatterns = [

	# Custom Views
	path('', IndexView.as_view(), name='index'),

	# Cuenta
	path('titulo/create/', BlankView.as_view(), name='create'),
	path('titulo/edit/<int:pk>/', BlankView.as_view(), name='cuenta'),

	# Comprobantes
	path('cbte/asiento/', BlankView.as_view(), name='cbte-create'),
	path('cbte/asiento/<int:pk>', BlankView.as_view(), name='cbte-edit'),
	
	# Registros
	path('registros/', RegistroView.as_view(), name='registros'),
	path('mayores/', MayoresView.as_view(), name='mayores'),	

]


