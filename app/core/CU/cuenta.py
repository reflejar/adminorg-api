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
from django_afip.models import CurrencyType


class CU:

	perfiles = ['cliente', 'proveedor']
	taxones = ['caja']

	def __init__(self, validate_data):

		self.validate_data = validate_data
		
		self.naturaleza = Naturaleza.objects.get(nombre=self.validate_data.pop('naturaleza'))

		if self.naturaleza.nombre in self.perfiles:
			self.perfil_data = self.validate_data.pop('perfil')
			self.perfil_data['comunidad'] = self.validate_data['comunidad']
			self.domicilio_data = self.perfil_data.pop('domicilio')
			self.tipo_documento = DocumentType.objects.get(description=self.perfil_data.pop('tipo_documento')) # Llega la data en forma de string y no como objeto
			prov = self.domicilio_data.pop('provincia')
			self.provincia = Provincia.objects.get(nombre=prov) if prov else None # Llega la data en forma de string y no como objeto

		# Para agarrar el taxon
		if self.naturaleza.nombre in ['caja']:
			self.validate_data['taxon'] = Taxon.objects.get(nombre=self.validate_data.pop('taxon'))
			self.validate_data['moneda'] = CurrencyType.objects.get(description=self.validate_data.pop('moneda'))
			
		
		self.validate_data['naturaleza'] = self.naturaleza

	
	def make_domicilio(self):
		# Esta funcion solo se ejecuta si el domicilio se establece en la cuenta y no en el perfil
		if self.naturaleza.nombre in self.perfiles:
			return Domicilio.objects.create(**self.domicilio_data, provincia=self.provincia)
		return


	def make_perfil(self):
		if self.naturaleza.nombre in self.perfiles:
			domicilio = Domicilio.objects.create(**self.domicilio_data, provincia=self.provincia)
			perfil = Perfil.objects.create(**self.perfil_data, domicilio=domicilio, tipo_documento=self.tipo_documento)
			return perfil
		return

	def get_clean_data(self): return self.validate_data
