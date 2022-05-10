from django.urls import include, path

from .views import *

urlpatterns = [


	# Custom Views
	path('', IndexView.as_view(), name='index'),
	path('<str:naturaleza>/', ListView.as_view(), name='list'),

]


