from datetime import date
from django.db import models
from utils.models import BaseModel
from django.apps import apps
from django.db.models import Q

class Proyecto(BaseModel):
	"""
	Modelo de proyecto
	"""
	nombre = models.CharField(max_length=100)

	def __str__(self): return str(self.nombre)