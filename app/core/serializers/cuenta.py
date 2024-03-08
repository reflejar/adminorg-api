from django.db import transaction
from rest_framework import serializers
from django_afip.models import DocumentType

from utils.serializers import DomicilioModelSerializer
from users.serializers import PerfilModelSerializer
from utils.models import (
	Comunidad,
	Provincia,
	Domicilio
)
from users.models import (
	Perfil,
)
from core.models import (
	Titulo,
	Taxon,
	Cuenta,
)
from core.serializers import (
	TituloModelSerializer,
)
from core.CU.cuenta import CU


class TaxonRelatedField(serializers.RelatedField):
    """
    Un campo personalizado para manejar la relación con el modelo Taxon
    utilizando el atributo 'nombre' en lugar de la clave primaria.
    """

    def to_representation(self, value):
        """
        Serialize la instancia de Taxon al nombre.
        """
        return value.nombre

    def to_internal_value(self, data):
        """
        Convierte el nombre en una instancia de Taxon.
        """
        return Taxon.objects.get(nombre=data)

class CuentaModelSerializer(serializers.ModelSerializer):
	"""
		Serializer de Cuenta
		Cuenta de naturaleza:
			Cliente
			Proveedor
			Caja
			Ingreso
			Gasto
	"""
	
	class Meta:
		model = Cuenta

		fields = ('id',)

	def __init__(self, *args, **kwargs):
		super(CuentaModelSerializer, self).__init__(*args, **kwargs)

		# Incorporacion de Nombre
		if self.context['naturaleza'] in ['caja', 'ingreso', 'gasto', 'bien_de_cambio']:
			self.fields['nombre'] = serializers.CharField(max_length=150, required=True)

		# Incorporacion de Numero
		if self.context['naturaleza'] in ['dominio']:
			self.fields['numero'] = serializers.IntegerField(read_only=False)

		# Incorporacion de Taxon
		if self.context['naturaleza'] in ['cliente', 'caja', 'ingreso', 'gasto']:
			self.fields['taxon'] = serializers.ChoiceField(required=True, choices=list(Taxon.objects.filter(naturaleza__nombre=self.context['naturaleza']).values_list('nombre', flat=True)))

		# Incorporacion de Perfil
		if self.context['naturaleza'] in ['cliente', 'proveedor']:
			self.fields['perfil'] = PerfilModelSerializer(read_only=False, context=self.context)


	def validate_nombre(self, nombre):
		"""
			No puede haber con el mismo nombre 
				cajas
				ingresos
				gastos
		"""


		query = Cuenta.objects.filter(
				comunidad=self.context['comunidad'], 
				nombre=nombre
			)

		if query and self.context['naturaleza'] in ['caja', 'ingreso', 'gasto']:
			if not self.instance in query:
				raise serializers.ValidationError('Ya existe una cuenta con el nombre solicitado')
		
		return nombre


	def validate_numero(self, numero):
		"""
			No puede haber con el mismo numero 
				clientes 
				dominios
				proveedores
		"""

		query = Cuenta.objects.filter(
				comunidad=self.context['comunidad'], 
				naturaleza__nombre=self.context['naturaleza'], 
				numero=numero
			)

		if query and self.context['naturaleza'] in ['dominio']:
			if not self.instance in query:
				raise serializers.ValidationError('Ya existe un {} con el numero solicitado'.format(self.context['naturaleza']))

		return numero


	def validate_perfil(self, perfil):
		"""
			No puede haber con el mismo numero_documento 
				clientes 
				proveedores
				Nota 07/09/2020. Se decidió que si se podia cargar con el mismo numero_documento
		"""

		# validacion conjunta (debe existir razon social, nombre o apellido)
		if self.context['naturaleza'] in ["cliente", "proveedor"]:
			if not 'apellido' in perfil.keys() and not 'razon_social' in perfil.keys():
				mj_error = ['Es necesario configurar un Nombre y Apellido o una Razón social']
				raise serializers.ValidationError({'apellido': mj_error})

		return perfil

	def validate(self, data):
		tipo = self.context['naturaleza'] if self.context['naturaleza'] != 'dominio' else 'cliente'
		try:
			data['titulo'] = Titulo.objects.get(comunidad=self.context['comunidad'], predeterminado__nombre=tipo)
		except:
			raise serializers.ValidationError({'titulo': 'Para agregar/modificar un nuevo {} es necesario configurar un Título Contable predeterminado'.format(self.context['naturaleza'])})



		return data

	@transaction.atomic
	def create(self, validate_data):
		"""
			Se construye un objeto completo de tipo dominio, cliente, proveedor, caja, ingreso o gasto.

			1 - Se crea Perfil y Domicilio en CU/cuenta/cuenta.
			2 - Se crea aqui la Cuenta
			3 - Se crean las vinculaciones de los dominios con los socios en CU/cuenta/cuenta. 
		"""

		validate_data['comunidad'] = self.context['comunidad']
		validate_data['naturaleza'] = self.context['naturaleza']

		cu = CU(validate_data)
		
		cuenta = Cuenta.objects.create(
			**cu.get_clean_data(),
			perfil=cu.make_perfil(),
			domicilio=cu.make_domicilio(),
			)

		return cuenta



	def update(self, instance, validate_data):
		"""
			Se actualiza: Cuenta, Perfil y Domicilio.
			Se construye un cliente completo.
		"""
			
		# Actualizacion de Nombre
		if self.context['naturaleza'] in ['caja', 'ingreso', 'gasto']:
			instance.nombre = validate_data['nombre']
				
		# Actualizacion de Numero
		if self.context['naturaleza'] in ['dominio']:
			instance.numero = validate_data['numero']

		# Actualizacion de Taxon
		if self.context['naturaleza'] in ['cliente', 'caja', 'ingreso', 'gasto']:
			instance.taxon = Taxon.objects.get(nombre=validate_data['taxon'])

		# Actualizacion de Perfil
		if self.context['naturaleza'] in ['cliente', 'proveedor']:		
			perfil = instance.perfil
			domicilio = perfil.domicilio
			perfil_data = validate_data['perfil']
			domicilio_data = perfil_data['domicilio']
			domicilio.provincia = Provincia.objects.get(nombre=domicilio_data['provincia'])
			domicilio.calle = domicilio_data.get('calle', domicilio.calle)
			domicilio.numero = domicilio_data.get('numero', domicilio.numero)
			domicilio.localidad = domicilio_data.get('localidad', domicilio.localidad)
			domicilio.save()
			perfil.nombre = perfil_data.get('nombre', perfil.nombre)
			perfil.apellido = perfil_data.get('apellido', perfil.apellido)
			perfil.razon_social = perfil_data.get('razon_social', perfil.razon_social)
			perfil.numero_documento = perfil_data.get('numero_documento', perfil.numero_documento)
			perfil.fecha_nacimiento = perfil_data.get('fecha_nacimiento', perfil.fecha_nacimiento)
			perfil.tipo_documento = DocumentType.objects.get(description=perfil_data['tipo_documento'])
			perfil.mail = perfil_data.get('mail', perfil.mail)
			perfil.telefono = perfil_data.get('telefono', perfil.telefono)
			perfil.comunidad = self.context['comunidad']
			perfil.domicilio = domicilio
			perfil.save()
			instance.perfil = perfil

		if self.context['naturaleza'] in ['dominio']:
			# Actualizacion de Domicilio (solo para Dominio)
			domicilio = instance.domicilio
			domicilio_data = validate_data['domicilio']
			domicilio.provincia = Provincia.objects.get(nombre=domicilio_data['provincia'])
			domicilio.calle = domicilio_data.get('calle', domicilio.calle)
			domicilio.numero = domicilio_data.get('numero', domicilio.numero)
			domicilio.localidad = domicilio_data.get('localidad', domicilio.localidad)
			domicilio.save()

		instance.save()

		# Actualizacion del titulo
		instance.titulo = validate_data['titulo']
		instance.save()



		return instance