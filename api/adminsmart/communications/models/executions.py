# Django
from django.db import models

# Custom
from .base import BaseCommunication


class Execution(BaseCommunication):
	"""
	Modelo para los envios realizados
	"""
	executed_at = models.DateTimeField(auto_now=True)
