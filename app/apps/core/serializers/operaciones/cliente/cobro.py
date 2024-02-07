from itertools import chain
from apps.core.serializers.operaciones.base import *
from apps.core.serializers.operaciones.cliente import CreditoModelSerializer


class CobroModelSerializer(OperacionModelSerializer):
	'''Operacion de debito cobrado a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		queryset = self.context['cuenta'].estado_deuda()
		if self.instance:
			queryset = list(chain(queryset, self.instance.cobros()))
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=queryset, 
				allow_null=False,
			)		
		self.fields['vinculo'].display_value = self.display_vinculo
		self.fields['origen'] = CreditoModelSerializer(context=self.context, read_only=True, many=False)