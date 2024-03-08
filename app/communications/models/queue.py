from datetime import timedelta

# Django
from django.db import models

# Custom
from .base import BaseCommunication
from ..gateway import Gateway
from .executions import Execution

from .. import constants


class Queue(BaseCommunication):
	"""
	Modelo para la cola de envios
	Cuando salga de aqui un envio puede enviarse
	por mail o hacia simple solutions
	"""


	OBS_MULTI_POSTPONE = "Too many attemps made!!"

	execute_at = models.DateTimeField(blank=True, null=True)
	tried = models.PositiveSmallIntegerField(default=1)

	def __str__(self):
		return "Envio: {}".format(self.subject)

	def perform_confirm(self, response):
		data = self.__dict__
		data.pop("execute_at")
		execution = Execution.objects.create(
			comunidad=self.comunidad,
			addressee=self.addressee,
			subject=self.subject,
			body=self.body,
			client=self.client,
			observations=response['status']
		)
		self.delete()

	def perform_postpone(self, response):
		post = response['post']
		if self.tried >= 5:
			self.observations = self.OBS_MULTI_POSTPONE
			self.execute_at = None
		else:
			self.tried += 1
			self.observations = response['status']
			self.execute_at += timedelta(minutes=post)
		self.save()

	def perform_error(self, response):
		self.observations = response['status']
		self.execute_at = None
		self.save()

	def exec(self):
		g = Gateway(
			addressee=self.addressee,
			subject=self.subject,
			body=self.body,
		)
		response = g.dispatch()
		try:
			{
				constants.CASE_OK: self.perform_confirm,
				constants.CASE_POSTPONE: self.perform_postpone,
			}[response['status']](response)
		except KeyError:
			self.perform_error(response)
