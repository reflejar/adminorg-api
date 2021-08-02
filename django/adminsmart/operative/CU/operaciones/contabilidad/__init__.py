from adminsmart.operative.models import Operacion
from adminsmart.utils.generics.functions import *

class CU:
	
	def __init__(self, documento, validated_data):
		self.documento = documento
		self.comunidad = documento.comunidad
		self.debe = validated_data['debe']
		self.haber = validated_data['haber']
		self.fecha = documento.receipt.issued_date
		self.identifier = randomIdentifier(Operacion, 'asiento')
		
		self.operaciones = []


	def hacer_debe(self):
		for i in self.debe:
			operacion_debe = Operacion(
				comunidad=self.comunidad,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
				fecha_indicativa=self.fecha,
				fecha=self.fecha,
			)
			self.operaciones.append(operacion_debe)


	def hacer_haber(self):
		for i in self.haber:
			operacion_haber = Operacion(
				comunidad=self.comunidad,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=i['cuenta'],
				valor=-i['monto'],
				detalle=i['detalle'],
				fecha_indicativa=self.fecha,
				fecha=self.fecha,
			)
			self.operaciones.append(operacion_haber)


	def create(self):
		self.hacer_debe()
		self.hacer_haber()
		Operacion.objects.bulk_create(self.operaciones)
		return Operacion.objects.filter(asiento=self.identifier)