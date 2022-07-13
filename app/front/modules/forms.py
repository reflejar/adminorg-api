from api.core.serializers import (
	CuentaModelSerializer,
	TituloModelSerializer,
	MetodoModelSerializer
)
from api.core.serializers.documentos import (
	DestinoClienteModelSerializer,
	OrigenProveedorModelSerializer,
	TesoroModelSerializer
)

from api.informes.serializer import (
	InformeSerializer
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

class DocumentoClienteForm(FormControl, DestinoClienteModelSerializer):
	pass

class DocumentoProveedorForm(FormControl, OrigenProveedorModelSerializer):
	pass

class DocumentoTesoreriaForm(FormControl, TesoroModelSerializer):
	pass

class InformeForm(FormControl, InformeSerializer):
	pass