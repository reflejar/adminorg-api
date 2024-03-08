from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.application import MIMEApplication

from .. import constants

class Dispatcher(object):

	ERROR_EMPTY_RECIPIENTS = "There is no destination for the shippment!"
	ERROR_COMUNIDAD_UNAUTHORIZED = "The community is not authorized to send mails!"

	def __init__(self, profile, subject, body, sender=settings.DEFAULT_FROM_EMAIL):
		self.sender = sender
		self.authorized = profile.comunidad.mails
		self.recipients = profile.get_emails_destinatarios()
		self.subject = subject
		self.body = body

	def send(self):
		if not self.authorized:
			return self.ERROR_COMUNIDAD_UNAUTHORIZED

		if len(self.recipients) > 0:
			for email in self.recipients:
				msg = EmailMultiAlternatives(
					subject=self.subject,
					body="",
					from_email=self.sender,
					to=[email],
				)
				msg.attach_alternative(self.body, "text/html")
				try:
					msg.send()
				except:
					return constants.CASE_POSTPONE
			return constants.CASE_OK
		else:
			return self.ERROR_EMPTY_RECIPIENTS

