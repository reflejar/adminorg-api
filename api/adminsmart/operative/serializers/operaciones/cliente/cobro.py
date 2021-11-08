from adminsmart.operative.serializers.operaciones.base import *
from adminsmart.operative.serializers.operaciones.cliente import CreditoModelSerializer


class CobroModelSerializer(OperacionModelSerializer):
	'''Operacion de debito cobrado a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=Operacion.objects.filter(
						comunidad=self.context['comunidad'], 
						cuenta__naturaleza__nombre__in=['cliente', 'dominio'],
					), 
				allow_null=False
			)		
		self.fields['origen'] = CreditoModelSerializer(context=self.context, read_only=True, many=False)
