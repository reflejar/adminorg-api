from apps.core.models import Operacion
from apps.utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.fecha_operacion = documento.fecha_operacion
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.punto_de_venta = self.comunidad.contribuyente.points_of_sales.get(number=self.receipt.point_of_sales)
		self.cargas = validated_data['cargas']
		self.cobros = validated_data['cobros']
		self.cajas = validated_data['cajas']
		self.resultados = validated_data['resultados']
		self.operaciones = []

	def hacer_cargas(self):
		print(self.cargas)

	def hacer_cobros(self):
		print(self.cobros)

	def hacer_cajas(self):
		print(self.cajas)

	def hacer_resultados(self):
		print(self.resultados)	

	def hacer_saldo_a_favor(self):
		print("hola")

	def create(self):
		
		self.hacer_cargas()
		
		self.hacer_cajas()

		self.hacer_resultados()

		self.hacer_saldo_a_favor()

		# bulk_create de las operaciones
		Operacion.objects.bulk_create(self.operaciones)
	
		return Operacion.objects.filter(asiento=self.identifier)


