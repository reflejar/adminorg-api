"""
Los envios en cola (Queue) cuando salen, salen por este gateway
"""
from communications import providers

class Gateway():

	DEFAULT_PROVIDER = providers.mail.Dispatcher

	def __init__(self, addressee, subject, body, **cases):
		self.addresse = addressee
		self.subject = subject
		self.body = body
		self.comunidad = self.addresse.comunidad
		self.cases = cases

	@property
	def dispatcher(self):
		# if self.comunidad.accountss_set.first():
		# 	return providers.simple_solutions.Dispatcher()
		return self.DEFAULT_PROVIDER(
			profile=self.addresse,
			subject=self.subject,
			body=self.body,
		)

	def dispatch(self):
		response = self.dispatcher.send()
		post = 60 if isinstance(response, str) else None
		return {
			'status': response, 
			'post': post
		}





