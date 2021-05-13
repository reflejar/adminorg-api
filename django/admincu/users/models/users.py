"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Adminsmart
from admincu.utils.models import BaseModel


class User(AbstractUser):

	"""
		Modelo de usuario propio
		Hereda de BaseModel
		Posibilidad de agregar nuevos atributos
		Hoy solo el is_verified
	"""

	is_verified = models.BooleanField(
		'verified',
		default=False,
		help_text='Set to true when the user have verified its email address.'
	)

	def __str__(self):
		"""Return username."""
		return self.username

	def get_short_name(self):
		"""Return username."""
		return self.username
