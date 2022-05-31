from adminsmart.api.core.serializers import (
	CuentaModelSerializer,
	TituloModelSerializer,
	MetodoModelSerializer
)


class FormControl:

	def __init__(self, *args, **kwargs):
		kwargs.pop('prefix')
		if 'files' in kwargs.keys():
			kwargs.pop('files')
		super().__init__(*args, **kwargs)

class CuentaForm(FormControl, CuentaModelSerializer):
	pass

class TituloForm(FormControl, TituloModelSerializer):
	pass

class MetodoForm(FormControl, MetodoModelSerializer):
	pass