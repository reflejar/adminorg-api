from adminsmart.core.serializers.operaciones.base import *
from adminsmart.core.serializers.operaciones.proveedor import DebitoModelSerializer


class PagoModelSerializer(OperacionModelSerializer):
	'''Operacion de debito cobrado a cliente'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=Operacion.objects.filter(
						comunidad=self.context['comunidad'], 
						cuenta__naturaleza__nombre='proveedor',
					), 
				allow_null=False
			)		
		self.fields['origen'] = DebitoModelSerializer(context=self.context, read_only=True, many=False)
				