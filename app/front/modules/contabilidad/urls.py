from django.urls import path

from ..base import BlankView

from .views import *

urlpatterns = [

	# Custom Views
	path('', IndexView.as_view(), name='index'),

	# Cuenta
	path('titulo/create/', CUDParametroView.as_view(), name='create'),
	path('titulo/edit/<int:pk>/', CUDParametroView.as_view(), name='cuenta'),

	# Comprobantes
	path('cbte/', BlankView.as_view(), name='cbte-create'),
	path('cbte/<int:pk>', BlankView.as_view(), name='cbte-edit'),
	
	# Registros
	path('registros/', RegistroView.as_view(), name='registros'),
	path('mayores/', MayoresView.as_view(), name='mayores'),	

]


