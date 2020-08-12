from .base import *

class TesoreriaViewSet(BaseViewSet):
	"""
		Documentos recibidos de Proveedores View Set.
			Todos los tipos de documento
		Crea, actualiza, detalla y lista Documentos.
	"""

	documentos = ['303']
	serializer_class = TesoroModelSerializer
	causante = 'caja'
	sin_destinatario = True


	@transaction.atomic
	def update(self, request, *args, **kwargs):
		obj = self.get_object()

		self.destroy_valid_pagos(obj)
		self.destroy_valid_disponibilidades(obj)

		return super().update(request, *args, **kwargs)

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ANULAR un Recibo X
			Se establece una validacion en la cual
				NO SE PUEDE ANULAR SI TIENE DISPONIBILIDADES QUE CREO EL DOCUMENTO Y POSTERIORMENTE FUERON UTILIZADOS
		"""
		
		obj = self.get_object()
		self.destroy_valid_anulado(obj)
		self.destroy_valid_disponibilidades(obj)

		raise serializers.ValidationError("El documento ya se encuentra anulado")
		obj.anular(self.get_fecha())
		return Response(status=status.HTTP_204_NO_CONTENT)			