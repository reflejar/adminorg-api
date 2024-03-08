# scripts/initial_data.py
import json
from datetime import date
from core.models import *
from django_afip.models import *
from django.contrib.auth.models import Group
from users.models import *
from utils.models import *

def crer_superusuario():
	"""Creación de superusuario"""
	username = input("username: ")
	password = input("password: ")
	nombre = input("nombre: ")
	apellido = input("apellido: ")
	email = input("email: ")
	superuser = User.objects.create(
		username=username,
		first_name=nombre,
		last_name=apellido,
		email=email,
		is_staff=True,
		is_active=True,
		is_superuser=True
	)

	superuser.set_password(password)
	superuser.save()


def crear_cosas_de_afip():
	"""Crear cosas necesarias para el funcionamiento de AFIP"""
	# Tipos de comprobantes
	receipt_types = open('scripts/receipt_types.json', 'r')
	data = json.load(receipt_types)
	for d in data:
		ReceiptType.objects.create(**d)

	# Tipos de conceptos
	concept_types = open('scripts/concept_types.json', 'r')
	data = json.load(concept_types)
	for d in data:
		ConceptType.objects.create(**d)		

	# Tipos de documento
	document_types = open('scripts/document_types.json', 'r')
	data = json.load(document_types)
	for d in data:
		DocumentType.objects.create(**d)		

	# Tipos de moneda
	currency_types = open('scripts/currency_types.json', 'r')
	data = json.load(currency_types)
	for d in data:
		CurrencyType.objects.create(**d)		


def crear_grupos():
	"""Crear grupos administrativo y socios"""
	Group.objects.create(
		name="administrativo"
	)	

def crear_cosas_core_de_aplicacion():
	"""Crear cosas necesarias para el funcionamiento del core"""
	# Crear Naturalezas
	naturalezas = open('scripts/naturalezas.json', 'r')
	data = json.load(naturalezas)
	for d in data:
		Naturaleza.objects.create(**d)

	# Crear Taxones
	taxones = open('scripts/taxones.json', 'r')
	data = json.load(taxones)
	for d in data:
		Taxon.objects.create(**d)				

	# Crear Provincias
	provincias = open('scripts/provincias.json', 'r')
	data = json.load(provincias)
	for d in data:
		Provincia.objects.create(**d)		

	# Crear Tipos de comunidad
	tipos_comunidad = open('scripts/tipos_comunidad.json', 'r')
	data = json.load(tipos_comunidad)
	for d in data:
		TipoComunidad.objects.create(**d)		

def crear_comunidad():
	"""Crear una nueva comunidad"""
	nombre = input("nombre de la comunidad: ")
	cuit = input("CUIT de la comunidad: ")
	provincia = input("Provincia de la comunidad: ")
	localidad = input("Localidad de la comunidad: ")
	calle = input("Domicilio de la comunidad: ")

	contribuyente = TaxPayer.objects.create(
		name=nombre,
		cuit=cuit,
		active_since=date.today(),
		is_sandboxed=True,
	)
	TaxPayerProfile.objects.create(
		taxpayer=contribuyente,
		issuing_name=nombre,
		issuing_address=calle,
		gross_income_condition=cuit,
		sales_terms="Cuenta corriente",
		vat_condition="IVA Exento"

	)
	PointOfSales.objects.create(
		number="0001",
		issuance_type="CAE - Exento",
		blocked=True,
		owner=contribuyente
	)

	domicilio = Domicilio.objects.create(
		provincia = Provincia.objects.get(nombre=provincia),
		localidad=localidad,
		calle=calle
	)

	comunidad = Comunidad.objects.create(
		id=9999,
		contribuyente=contribuyente,
		nombre=nombre,
		abreviatura=nombre.lower()[:5],
		tipo=TipoComunidad.objects.get(codigo_afip="0"),
		domicilio=domicilio
	)

	# Crear Plan de cuentas basico
	plan_cuentas = open('scripts/plan_cuentas.json', 'r')
	data = json.load(plan_cuentas)
	for d in data:
		d['comunidad_id'] = comunidad.id
		Titulo.objects.create(**d)				
		
	# Crear usuario administrativo?
	username = input("Usuario administrativo - username: ")
	password = input("Usuario administrativo - password: ")
	nombre = input("Usuario administrativo - nombre: ")
	apellido = input("Usuario administrativo - apellido: ")
	email = input("Usuario administrativo - email: ")
	user_admin = User.objects.create(
		username=username,
		first_name=nombre,
		last_name=apellido,
		email=email,
		is_active=True,
		is_verified=True,
	)
	user_admin.set_password(password)
	user_admin.save()
	user_admin.groups.add(Group.objects.get(name='administrativo'))

	perfil_admin = Perfil.objects.create(
		comunidad=comunidad,
		nombre=nombre,
		apellido=apellido,
		numero_documento="00000000",
	)
	perfil_admin.users.add(user_admin)

def run():
	solicitudes = [
		crer_superusuario,
		crear_cosas_de_afip,
		crear_grupos,
		crear_cosas_core_de_aplicacion,
		crear_comunidad,
	]
	for func in solicitudes:
		nombre_funcion = ' '.join(func.__name__.split('_'))
		print("#########################")
		print(func.__doc__)
		consulta = input(f"¿Querés {nombre_funcion}? ('s' para crear / nada para cancelar): ")
		if consulta.lower() == "s":
			func()
		else:
			print(" ".join([nombre_funcion, "cancelada"]))
	print("¡Instalación terminada!")


	


	
	
	# Crear cosas de Utils: Modulos, Provincias, Tipos de Comunidad 

