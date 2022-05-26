from django.urls import include, path

from .views import *

urlpatterns = [


	# Custom Views
	path('', IndexView.as_view(), name='index'),
	path('<str:naturaleza>/', ListView.as_view(), name='list'),
	path('<str:naturaleza>/create', CUDObjectView.as_view(), name='create'),
	path('<str:naturaleza>/<int:pk>/edit', CUDObjectView.as_view(), name='edit'),
	path('<str:naturaleza>/<int:pk>/delete', CUDObjectView.as_view(), name='delete'),

]


