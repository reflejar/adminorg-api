from django_afip.models import DocumentType

from adminsmart.apps.utils.models import (
	Provincia,
	Domicilio
)
from adminsmart.apps.users.models import (
	Perfil,
)
from adminsmart.apps.core.models import (
	Titulo,
	Taxon,
	Naturaleza,
	Cuenta,
	Metodo,
	DefinicionVinculo
)


class CU:

	perfiles = ['cliente', 'proveedor']
	domicilios = ['dominio']
	metodos = ['proveedor', 'ingreso']
	taxones = ['cliente', 'caja', 'ingreso', 'gasto']
	vinculaciones = ['dominio']

	def __init__(self, validate_data):

		self.validate_data = validate_data
		
		self.naturaleza = Naturaleza.objects.get(nombre=self.validate_data.pop('naturaleza'))

		# Para ver desde donde se toman los datos para el domicilio
		if self.naturaleza.nombre in self.domicilios:
			self.domicilio_data = self.validate_data.pop('domicilio')
			self.provincia = Provincia.objects.get(nombre=self.domicilio_data.pop('provincia')) # Llega la data en forma de string y no como objeto

		elif self.naturaleza.nombre in self.perfiles:
			self.perfil_data = self.validate_data.pop('perfil')
			self.perfil_data['comunidad'] = self.validate_data['comunidad']
			self.domicilio_data = self.perfil_data.pop('domicilio')
			self.tipo_documento = DocumentType.objects.get(description=self.perfil_data.pop('tipo_documento')) # Llega la data en forma de string y no como objeto
			self.provincia = Provincia.objects.get(nombre=self.domicilio_data.pop('provincia')) # Llega la data en forma de string y no como objeto

		# Para agarrar el taxon
		self.taxon = Taxon.objects.get(nombre=self.validate_data.pop('taxon')) if self.naturaleza.nombre in self.taxones else None

		# Para agarrar los metodos
		self.metodos_data = []
		if self.naturaleza.nombre == "ingreso":
			self.metodos_data.append(self.validate_data.pop('interes'))
			self.metodos_data.append(self.validate_data.pop('descuento'))

		elif self.naturaleza.nombre == "proveedor":
			for r in self.validate_data.pop('retiene'):
				self.metodos_data.append(r)

		# Para agarrar las vinculaciones
		if self.naturaleza.nombre in self.vinculaciones:
			self.vinculos_data = [
				{
				'definicion': "propietario",
				'cuenta_vinculada': self.validate_data.pop('propietario'),
				},
				{
				'definicion': "inquilino",
				'cuenta_vinculada': self.validate_data.pop('inquilino'),
				}
			]
		else:
			self.vinculos_data = []
	
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

	def get_metodos(self):
		
		return filter(lambda x: x!=None, self.metodos_data)

	def make_vinculaciones(self, cuenta):
		for v in self.vinculos_data:
			if v['cuenta_vinculada']:
				vinculo = DefinicionVinculo.objects.create(
					cuenta=v['cuenta_vinculada'], # Socio
					cuenta_vinculada=cuenta, # Dominio
					definicion=Taxon.objects.get(nombre=v['definicion']),
					)
				