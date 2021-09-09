from django.contrib.auth.models import Group
from django_afip.models import DocumentType

from adminsmart.users.models import *
from adminsmart.utils.models import Comunidad


class UsersSetUp():

	DEFAULT_USERNAME = "demo"
	DEFAULT_USER_EMAIL = "demo@demo.com"
	DEFAULT_GROUP = "administrativo"
	DEFAULT_PROFILE_NAME = "Demo"
	DEFAULT_DOCUMENT_TYPE = "DNI"
	DEFAULT_DOCUMENT_NUMBER = "11222333"

	def create_group(self):
		self.group = Group.objects.create(name=self.DEFAULT_GROUP)

	def create_user(self, username=None):
		username = username or self.DEFAULT_USERNAME
		self.user = User.objects.create(
			username=username,
			first_name=username,
			last_name=username,
			is_verified=True,
			email=self.DEFAULT_USER_EMAIL
		)
		self.user.set_password(username+username)
		self.user.save()
		self.user.groups.add(self.group)

	def create_document_type(self):
		self.document_type = DocumentType.objects.create(
			code=96,
			description=self.DEFAULT_DOCUMENT_TYPE
		)

	def create_profile(self):
		self.profile = Perfil.objects.create(
			nombre=self.DEFAULT_PROFILE_NAME,
			apellido=self.DEFAULT_PROFILE_NAME,
			tipo_documento=self.document_type,
			numero_documento=self.DEFAULT_DOCUMENT_NUMBER,
			comunidad=Comunidad.objects.get(nombre=self.DEFAULT_PROFILE_NAME)
		)
		self.profile.users.add(self.user)

	def __create__(self):
		self.create_group()
		self.create_user()
		self.create_document_type()
		self.create_profile()