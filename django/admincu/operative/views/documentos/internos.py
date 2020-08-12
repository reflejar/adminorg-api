from .base import *


class InternoViewSet(BaseViewSet):

	documentos = ['303', '400']
	serializer_class = InternoModelSerializer
	causante = 'interno'
	sin_destinatario = True


	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ANULAR una TRANSFERENCIA o ELIMINAR un asiento
		"""
		obj = self.get_object()

		if obj.receipt.receipt_type.code == "303":
			obj.anular(self.get_fecha())
		else:
			obj.eliminar()
		return Response(status=status.HTTP_204_NO_CONTENT)	