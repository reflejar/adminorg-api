from adminsmart.utils.models import *

class BasicSetUp():

	DEFAULT_NAME_COMUNIDAD = "Demo"
	DEFAULT_PROVINCIA = "SALTA"
	DEFAULT_TIPO_COMUNIDAD = "CLUB DE CAMPO"

	def create_domicilio(self):
		self.provincia = Provincia.objects.create(
			nombre=self.DEFAULT_PROVINCIA,
			codigo_afip=9
		)
		self.domicilio = Domicilio.objects.create(
			provincia=self.provincia,
			calle=self.DEFAULT_NAME_COMUNIDAD,
			numero=13
		)

	def create_tipo_comunidad(self):
		self.tipo = TipoComunidad.objects.create(
			codigo_afip=5,
			nombre=self.DEFAULT_TIPO_COMUNIDAD
		)

	def create_comunidad(self, name=None):
		name = name or self.DEFAULT_NAME_COMUNIDAD
		self.comunidad = Comunidad.objects.create(
			nombre=name,
			domicilio=self.domicilio,
			tipo=self.tipo,
			abreviatura=name.lower()[:5],
			mails=False,
		)

	def __create__(self):
		self.create_domicilio()
		self.create_tipo_comunidad()
		self.create_comunidad()