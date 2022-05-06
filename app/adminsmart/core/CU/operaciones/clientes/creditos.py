from adminsmart.core.models import Operacion
from adminsmart.utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.comunidad = documento.comunidad
		self.creditos = validated_data['creditos']
		self.identifier = randomIdentifier(Operacion, 'asiento')

	def get_metodo(self, cuenta, naturaleza):
		
		try:
			return cuenta.metodos.get(naturaleza=naturaleza)
		except:
			return


	def create(self):
		operaciones = []
		for credito in self.creditos:
			metodo_interes = self.get_metodo(cuenta=credito['concepto'], naturaleza='interes')
			metodo_descuento = self.get_metodo(cuenta=credito['concepto'], naturaleza='descuento') 
			operacion_debe = Operacion.objects.create(
				comunidad=self.comunidad,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=credito['destinatario'],
				cantidad=credito['cantidad'],
				valor=credito['monto'],
				detalle=credito['detalle'],
				fecha=self.documento.fecha_operacion,
				fecha_indicativa=credito['periodo'] or self.documento.fecha_operacion,
				fecha_gracia=credito['fecha_gracia'],
				fecha_vencimiento=credito['fecha_vencimiento'],
			)
			if metodo_interes:
				operacion_debe.metodos.add(metodo_interes)
			if metodo_descuento:
				operacion_debe.metodos.add(metodo_descuento)
			
			operaciones.append(operacion_debe)
			operacion_haber = Operacion.objects.create(
				comunidad=self.comunidad,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=credito['concepto'],
				valor=-credito['monto'],
				detalle=credito['detalle'],
				vinculo=operacion_debe,
				fecha=self.documento.fecha_operacion,
				fecha_indicativa=credito['periodo'] or self.documento.fecha_operacion,
				)
			operaciones.append(operacion_haber)

		return operaciones