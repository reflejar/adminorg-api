# Django
from django.db import models

# Custom
from utils.models import BaseModel

class Queue(BaseModel):
	"""
		Modelo para la cola de envios
		Cuando salga de aqui un envio puede enviarse 
			por mail o hacia simple solutions
	"""

	addressee = models.ForeignKey('users.Perfil')
	subject = models.CharField(max_length=100, blank=True, null=True)
	body = models.TextField(blank=True, null=True)
	model = models.CharField(max_length=100, blank=True, null=True)
	instance = models.IntegerField(blank=True, null=True)
	attach = models.CharField(max_length=100, blank=True, null=True) # Un string con una lista de atributos con files
	observations = models.TextField(blank=True, null=True)
	send_at = models.DateTimeField(blank=True, null=True)

	def send(self):
		pass


class Sent(BaseModel):
	"""
		Modelo para los envios realizados
	"""

	instance = models.ForeignKey('communications.Queue')
	observations = models.TextField(blank=True, null=True)
	sent_on = models.DateTimeField(blank=True, null=True)