from .base import *

class ProveedorViewSet(BaseViewSet):
	"""
		Documentos recibidos de Proveedores View Set.
			Todos los tipos de documento
		Crea, actualiza, detalla y lista Documentos.
	"""

	documentos = list(ReceiptType.objects.all().values_list('code', flat=True))
	serializer_class = OrigenProveedorModelSerializer
	causante = 'proveedor'


	@transaction.atomic
	def update(self, request, *args, **kwargs):
		obj = self.get_object()
		# if obj.receipt.receipt_type.code == "301":
		# 	raise serializers.ValidationError("No se puede modificar un documento de tipo {}".format(obj.receipt.receipt_type))

		self.destroy_valid_pagos(obj)

		return super().update(request, *args, **kwargs)

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ANULAR una ORDEN DE PAGO o ELIMINAR una deuda
			Se establece una validacion en la cual
				NO SE PUEDE ANULAR SI YA TIENE DOCUMENTOS POSTERIORES VINCULADOS
		"""
		obj = self.get_object()

		self.destroy_valid_anulado(obj)
		self.destroy_valid_pagos(obj)
		self.destroy_valid_saldos(obj)
		
		if obj.receipt.receipt_type.code == "301":
			obj.anular(self.get_fecha())
		else:
			obj.eliminar()
		return Response(status=status.HTTP_204_NO_CONTENT)
	