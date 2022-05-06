from adminsmart.core.models import Operacion, Documento, Cuenta
from typing import Dict, Any, Union
from decimal import Decimal

class EstadoBaseSerializer:

	def __init__(self, queryset, context):
		self.queryset = queryset
		self.context = context

	@property
	def data(self):
		return [self.makeJSON(o) for o in self.queryset]