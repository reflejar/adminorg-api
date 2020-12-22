from datetime import date

from admincu.operative.serializers.operaciones.base import *
from admincu.operative.serializers.estados.deudas import EstadoDeudasModelSerializer


class UtilizacionModelSerializer(OperacionModelSerializer):
	'''Operacion de utilizacion de saldo a favor o cheques'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=Operacion.objects.filter(
						comunidad=self.context['comunidad'], 
						cuenta__naturaleza__nombre__in=['cliente', 'caja', 'proveedor'],
					), 
				allow_null=False
			)
		if 'retrieve' in self.context.keys():
			self.fields['origen'] = EstadoDeudasModelSerializer(context=self.context, read_only=True, many=False)
			self.context['fecha'] = date.today()
			self.context['condonacion'] = False
			self.context['causante'] = "estado"
