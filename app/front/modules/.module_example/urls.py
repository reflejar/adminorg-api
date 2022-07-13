from django.urls import path

from ..base import BlankView

from .views import *

urlpatterns = [

	# Custom Views
	path('', IndexView.as_view(), name='index'),	

]


