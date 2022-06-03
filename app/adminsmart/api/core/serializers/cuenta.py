from django.db import transaction
from rest_framework import serializers
from django_afip.models import DocumentType

from adminsmart.api.utils.serializers import DomicilioModelSerializer
from adminsmart.api.users.serializers import PerfilModelSerializer
from adminsmart.apps.utils.models import (
	Comunidad,
	Provincia,
	Domicilio
)
from adminsmart.apps.users.models import (
	Perfil,
)
from adminsmart.apps.core.models import (
	Titulo,
	Taxon,

	Cuenta,
	Metodo,
	DefinicionVinculo
)
from adminsmart.api.core.serializers import (
	VinculoModelSerializer,
	MetodoModelSerializer,
	TituloModelSerializer,
)
from adminsmart.apps.core.CU.cuenta import CU


class CuentaModelSerializer(serializers.ModelSerializer):
	"""
		Serializer de Cuenta
		Cuenta de naturaleza:
			Dominio
			Cliente
			Proveedor
			Caja
			Ingreso
			Gasto
	"""
	
	class Meta:
		model = Cuenta

		fields = (
			'id',
			'titulo'
		)

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
			self.fields['taxon'] = serializers.PrimaryKeyRelatedField(
					queryset=Taxon.objects.filter(naturaleza__nombre=self.context['naturaleza']), 
					label="Tipo",
					required=True
				)

		# Incorporacion de Perfil
		if self.context['naturaleza'] in ['cliente', 'proveedor']:
			self.fields['perfil'] = PerfilModelSerializer(read_only=False)

		# Incorporacion de Domicilio (solo para Dominio)
		if self.context['naturaleza'] in ['dominio']:
			self.fields['domicilio'] = DomicilioModelSerializer(read_only=False)

		# Incorporacion de Metodos
		if self.context['naturaleza'] == 'proveedor':
			self.fields['retiene'] = serializers.PrimaryKeyRelatedField(queryset=Metodo.objects.filter(comunidad=self.context['comunidad'], naturaleza="retencion"), many=True)
		elif self.context['naturaleza'] == 'ingreso':
			self.fields['interes'] = serializers.PrimaryKeyRelatedField(
					queryset=Metodo.objects.filter(comunidad=self.context['comunidad'], naturaleza="interes"), 
					label="Metodología de intereses",
					allow_null=True
				)
			self.fields['descuento'] = serializers.PrimaryKeyRelatedField(
					queryset=Metodo.objects.filter(comunidad=self.context['comunidad'], naturaleza="descuento"), 
					label="Metodología de descuentos",
					allow_null=True
				)
	
		# Incorporacion de Propietario y Ocupante (para Dominios)
		if self.context['naturaleza'] in ['dominio']:
			self.fields['propietario'] = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.filter(comunidad=self.context['comunidad'], naturaleza__nombre="cliente"), allow_null=True)
			self.fields['inquilino'] = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.filter(comunidad=self.context['comunidad'], naturaleza__nombre="cliente"), allow_null=True)

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

		if self.context['naturaleza'] in ['dominio', 'cliente', 'proveedor']:
			try:
				query = Cuenta.objects.get(
							comunidad=self.context['comunidad'], 
							naturaleza__nombre=self.context['naturaleza'], 
							numero=numero
						)
			except:
				query = None

			if query:
				if self.context['request'].method == 'POST' or self.instance != query:
					raise serializers.ValidationError('Ya existe un {} con el numero solicitado'.format(self.context['naturaleza']))

		return numero


	def validate_perfil(self, perfil):
		"""
			No puede haber con el mismo numero_documento 
				clientes 
				proveedores
				Nota 07/09/2020. Se decidió que si se podia cargar con el mismo numero_documento
		"""


		# if self.context['naturaleza'] in ['cliente', 'proveedor']:
		# 	try:
		# 		query = Cuenta.objects.get(
		# 					comunidad=self.context['comunidad'],
		# 					perfil__numero_documento=perfil['numero_documento'], 
		# 					naturaleza__nombre=self.context['naturaleza'], 
		# 				)
		# 	except:
		# 		query = None
			
		# 	if query:
		# 		if self.context['request'].method == 'POST' or self.instance != query:
		# 			raise serializers.ValidationError({'numero_documento': 'El numero de documento seleccionado ya existe en el sistema'})
						
		return perfil

	def validate_retiene(self, retiene):
		"""
			No puede haber con los mismos retiene 
				proveedores
		"""

		if self.context['naturaleza'] == 'proveedor':
			for r in retiene:
				query = Cuenta.objects.filter(
						comunidad=self.context['comunidad'],
						naturaleza__nombre=self.context['naturaleza'], 
						metodos=r
					)
				if query:
					if self.context['request'].method == 'POST' or self.instance != query:
						raise serializers.ValidationError('El metodo seleccionado ya pertenece a otro proveedor')
		
		return retiene

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
		for metodo in cu.get_metodos():
			cuenta.metodos.add(metodo)

		cu.make_vinculaciones(cuenta)

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

			# # Actualizacion de las vinculaciones
			for v in DefinicionVinculo.objects.filter(cuenta_vinculada=instance):
				v.delete()
			vinculos_data = [
				{
				'definicion': "propietario",
				'cuenta_vinculada': validate_data.pop('propietario'),
				},
				{
				'definicion': "inquilino",
				'cuenta_vinculada': validate_data.pop('inquilino'),
				}
			]			
			for v in vinculos_data:
				if v['cuenta_vinculada']:
					vinculo = DefinicionVinculo.objects.create(
						cuenta=v['cuenta_vinculada'], # Socio
						cuenta_vinculada=instance, # Dominio
						definicion=Taxon.objects.get(nombre=v['definicion']),
						)			

		instance.save()
		
		# Actualizacion de Metodos 
		if self.context['naturaleza'] in ['proveedor', 'ingreso']:
			for m in instance.metodos.all():
				instance.metodos.remove(m)

			if self.context['naturaleza'] == 'proveedor':
				retiene_data = validate_data['retiene']
				for r in retiene_data:
					instance.metodos.add(r)
			elif self.context['naturaleza'] == 'ingreso':
				descuento_data = validate_data['descuento']
				if descuento_data:
					instance.metodos.add(descuento_data)
				interes_data = validate_data['interes']
				if interes_data:
					instance.metodos.add(interes_data)

		# Actualizacion del titulo
		instance.titulo = validate_data['titulo']
		instance.save()
		# if self.context['naturaleza'] in ['cliente']:
		# 	for v in instance.vinculos.all():
		# 		instance.vinculos.remove(v)
		
		# 	vinculaciones_data = validate_data['vinculaciones']
		# 	for v in vinculaciones_data:
		# 		taxon = Taxon.objects.get(nombre=v['definicion'])
		# 		vinculo = DefinicionVinculo.objects.create(
		# 				cuenta=instance,
		# 				cuenta_vinculada=v['cuenta_vinculada'],
		# 				definicion=taxon,
		# 				)


		return instance