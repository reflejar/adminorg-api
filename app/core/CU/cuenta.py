from django_afip.models import DocumentType

from utils.models import (
	Provincia,
	Domicilio
)
from users.models import (
	Perfil,
)
from core.models import (
	Titulo,
	Taxon,
	Naturaleza,
	Cuenta,
)


class CU:

	perfiles = ['cliente', 'proveedor']
	domicilios = ['cliente', 'proveedor']
	taxones = ['cliente', 'caja', 'ingreso', 'gasto']

	def __init__(self, validate_data):

		self.validate_data = validate_data
		
		self.naturaleza = Naturaleza.objects.get(nombre=self.validate_data.pop('naturaleza'))

		if self.naturaleza.nombre in self.perfiles:
			self.perfil_data = self.validate_data.pop('perfil')
			self.perfil_data['comunidad'] = self.validate_data['comunidad']
			self.domicilio_data = self.perfil_data.pop('domicilio')
			self.tipo_documento = DocumentType.objects.get(description=self.perfil_data.pop('tipo_documento')) # Llega la data en forma de string y no como objeto
			self.provincia = Provincia.objects.get(nombre=self.domicilio_data.pop('provincia')) # Llega la data en forma de string y no como objeto

		# Para agarrar el taxon
		self.taxon = Taxon.objects.get(nombre=self.validate_data.pop('taxon')) if self.naturaleza.nombre in self.taxones else None

	
	def make_domicilio(self):
		# Esta funcion solo se ejecuta si el domicilio se establece en la cuenta y no en el perfil
		if self.naturaleza.nombre in self.domicilios:
			return Domicilio.objects.create(**self.domicilio_data, provincia=self.provincia)
		return


	def make_perfil(self):
		if self.naturaleza.nombre in self.perfiles:
			domicilio = Domicilio.objects.create(**self.domicilio_data, provincia=self.provincia)
			perfil = Perfil.objects.create(**self.perfil_data, domicilio=domicilio, tipo_documento=self.tipo_documento)
			return perfil
		return

	def get_clean_data(self):
		
		self.validate_data['naturaleza'] = self.naturaleza
		self.validate_data['taxon'] = self.taxon
		
		return self.validate_data
