# scripts/initial_data.py
from apps.core.models import *

def run():
	# Crear objetos solicitando los datos
    # De afip crear Contribuyente, TaxPayerProfile, TaxPayerExtra, Punto de Venta
	# De utils crear Comunidad y Domicilio y crearle plan de cuentas basico
	comunidad = input("Nombre de la comunidad: ")
	print(comunidad)