from admincu.operative.serializers.operaciones.base import *

from admincu.operative.models import Metodo

from admincu.operative.serializers.metodo import MetodoModelSerializer

class RetencionModelSerializer(OperacionModelSerializer):
	'''Operacion de debito realizada con proveedores'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['retencion'] = serializers.PrimaryKeyRelatedField(
				queryset=Metodo.objects.filter(
						comunidad=self.context['comunidad'], 
						naturaleza="retencion"
					), 
				allow_null=False
			)
		self.fields.pop('detalle')
		self.fields['detalle'] = serializers.CharField(max_length=150, read_only=True)
		self.context['naturaleza'] = "retencion"
		self.fields['retencion'] = MetodoModelSerializer(context=self.context, read_only=True, many=False)
				