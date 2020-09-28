from .base import *


class AsientoViewSet(BaseViewSet):

	documentos = ['400']
	serializer_class = AsientoModelSerializer
	causante = 'asiento'
	sin_destinatario = True


	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ELIMINAR un asiento
		"""
		obj = self.get_object()

		obj.eliminar()
		return Response(status=status.HTTP_204_NO_CONTENT)	