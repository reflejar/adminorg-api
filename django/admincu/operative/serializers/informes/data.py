from rest_framework import serializers

from admincu.operative.models import Operacion
from admincu.operative.serializers.operaciones.calculator import *

"""

Hacer que herede de OperacionModelSerializer
que OperacionModelSerializer tenga todos los calculos.
Inspeccionar que pasa con sobreescribir las cosas


"""

class InformesModelSerializer(CalculatorModelSerializer):
	
	'''Operacion para la parte informes'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields.pop('pago_capital')
		# Si se decide que se exporte el SALDO, INTERES y TOTAL, se tiene que buscar una buena forma 
		# que no tome tanto tiempo de calculo
		self.fields.pop('saldo')
		self.fields.pop('interes')
		self.fields.pop('total')