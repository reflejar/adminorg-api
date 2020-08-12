from django.db import transaction
from rest_framework import serializers
from django_afip.models import DocumentType

from admincu.utils.serializers import DomicilioModelSerializer
from admincu.users.serializers import PerfilModelSerializer
from admincu.utils.models import (
	Comunidad,
	Provincia,
	Domicilio
)
from admincu.users.models import (
	Perfil,
)
from admincu.operative.models import (
	Titulo,
	Taxon,

	Cuenta,
	Metodo,
	DefinicionVinculo
)
from admincu.operative.serializers import (
	VinculoModelSerializer,
	MetodoModelSerializer,
	TituloModelSerializer,
)
from admincu.operative.CU.cuenta import CU


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
		if self.context['naturaleza'] in ['caja', 'ingreso', 'gasto', 'dominio']:
			self.fields['nombre'] = serializers.CharField(max_length=150, required=True)

		# Incorporacion de Numero
		if self.context['naturaleza'] in ['dominio']:
			self.fields['numero'] = serializers.IntegerField(read_only=False)

		# Incorporacion de Taxon
		if self.context['naturaleza'] in ['cliente', 'caja', 'ingreso', 'gasto']:
			self.fields['taxon'] = serializers.ChoiceField(required=True, choices=list(Taxon.objects.filter(naturaleza__nombre=self.context['naturaleza']).values_list('nombre', flat=True)))

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
			self.fields['interes'] = serializers.PrimaryKeyRelatedField(queryset=Metodo.objects.filter(comunidad=self.context['comunidad'], naturaleza="interes"), allow_null=True)
			self.fields['descuento'] = serializers.PrimaryKeyRelatedField(queryset=Metodo.objects.filter(comunidad=self.context['comunidad'], naturaleza="descuento"), allow_null=True)
	
		# Incorporacion de Vinculaciones (para Socios)
		if self.context['naturaleza'] in ['cliente']:
		 	self.fields['vinculaciones'] = VinculoModelSerializer(context=self.context, read_only=False, many=True)

		# Incorporacion de Propietario y Ocupante (para Dominios) - Solo Lectura
		if self.context['naturaleza'] in ['dominio']:
			self.fields['propietario'] = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.filter(comunidad=self.context['comunidad'], naturaleza__nombre="cliente"), allow_null=True)
			self.fields.get('propietario').read_only = True
			self.fields['ocupante'] = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.filter(comunidad=self.context['comunidad'], naturaleza__nombre="cliente"), allow_null=True)
			self.fields.get('ocupante').read_only = True

	def validate_nombre(self, nombre):
		"""
			No puede haber con el mismo nombre 
				cajas
				ingresos
				gastos
		"""

		if self.context['request'].method == 'POST':
			if self.context['naturaleza'] in ['caja', 'ingreso', 'gasto']:
				if Cuenta.objects.filter(
					comunidad=self.context['comunidad'], 
					naturaleza__nombre=self.context['naturaleza'], 
					nombre=nombre
				):			
					raise serializers.ValidationError('Ya existe un {} con el nombre solicitado'.format(self.context['naturaleza']))
		
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
		"""

		if self.context['naturaleza'] in ['cliente', 'proveedor']:
			try:
				query = Cuenta.objects.get(
							comunidad=self.context['comunidad'],
							perfil__numero_documento=perfil['numero_documento'], 
							naturaleza__nombre=self.context['naturaleza'], 
						)
			except:
				query = None
			
			if query:
				if self.context['request'].method == 'POST' or self.instance != query:
					raise serializers.ValidationError('El numero de documento seleccionado ya existe en el sistema')
		
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

	def validate_vinculaciones(self, vinculaciones):
		"""
			En la creacion de un cliente solo se pueden agregar vinculaciones (dominios) como
				ocupante
				propietario
			siempre y cuando los mismos no esten ya en la misma condicion con otro cliente
		"""
		
		for v in vinculaciones:

			ocupante = v['cuenta_vinculada'].ocupante()
			if v['definicion'] == "ocupante" and ocupante:
				if self.context['request'].method == 'POST' or self.instance != ocupante:
					raise serializers.ValidationError('El dominio numero {} ya posee un ocupante'.format(v["cuenta_vinculada"].numero))
			
			propietario = v['cuenta_vinculada'].propietario()
			if v['definicion'] == "propietario" and propietario:
				if self.context['request'].method == 'POST' or self.instance != propietario:
					raise serializers.ValidationError('El dominio numero {} ya posee un propietario'.format(v["cuenta_vinculada"].numero))

		return vinculaciones

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
		if self.context['naturaleza'] in ['caja', 'ingreso', 'gasto', 'dominio']:
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
			instance.titulo = validate_data['titulo']
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

		# Actualizacion de Domicilio (solo para Dominio)
		if self.context['naturaleza'] in ['dominio']:
			domicilio = instance.domicilio
			domicilio_data = validate_data['domicilio']
			domicilio.provincia = Provincia.objects.get(nombre=domicilio_data['provincia'])
			domicilio.calle = domicilio_data.get('calle', domicilio.calle)
			domicilio.numero = domicilio_data.get('numero', domicilio.numero)
			domicilio.localidad = domicilio_data.get('localidad', domicilio.localidad)
			domicilio.save()

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
				instance.metodos.add(descuento_data)
				interes_data = validate_data['interes']
				instance.metodos.add(interes_data)


		if self.context['naturaleza'] in ['cliente']:
			for v in instance.vinculos.all():
				instance.vinculos.remove(v)
		
			vinculaciones_data = validate_data['vinculaciones']
			for v in vinculaciones_data:
				taxon = Taxon.objects.get(nombre=v['definicion'])
				vinculo = DefinicionVinculo.objects.create(
						cuenta=instance,
						cuenta_vinculada=v['cuenta_vinculada'],
						definicion=taxon,
						)


		return instance