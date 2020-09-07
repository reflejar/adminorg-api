from .base import *
from rest_framework.decorators import action

from admincu.taskapp.tasks import facturacion_masiva

class ClienteViewSet(BaseViewSet):
	"""
		Documentos para Clientes View Set.
			Facturas: 11 y 51
			Nota de Debito: 12 y 52
			Nota de Credito: 13 y 53
			Recibo X: 54
		Crea, no actualiza, detalla y lista Documentos.
	"""

	http_method_names = ['get', 'post', 'delete']
	documentos = ['11', '12', '13', '51', '52', '53', '54']
	serializer_class = DestinoClienteModelSerializer
	causante = 'cliente'

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ANULAR un Recibo X
			Se establece una validacion en la cual
				NO SE PUEDE ANULAR SI TIENE SALDOS A FAVOR QUE POSTERIORMENTE FUERON UTILIZADOS
		"""
		
		obj = self.get_object()

		if obj.receipt.receipt_type.code != "54":
			raise serializers.ValidationError("No se puede anular un documento de tipo {}".format(obj.receipt.receipt_type))

		self.destroy_valid_anulado(obj)
		self.destroy_valid_saldos(obj)
		self.destroy_valid_disponibilidades(obj)

		raise serializers.ValidationError("El documento ya se encuentra anulado")
		obj.anular(self.get_fecha())
		return Response(status=status.HTTP_204_NO_CONTENT)	



	@action(detail=False, methods=['post'])
	def masivo(self, request, *args, **kwargs):
		""" Facturacion masiva """
		if kwargs['code'] != "11":
			raise serializers.ValidationError("Solo se pueden realizar Facturas C en forma masiva")
		
		self.causante = "cliente-masivo"
		self.sin_destinatario = True

		serializer = MasivoClienteModelSerializer(data=request.data, context=self.get_serializer_context())
		serializer.is_valid(raise_exception=True)
		context = {
			'causante': self.causante,
			'sin_destinatario': self.sin_destinatario,
			'receipt_type': self.kwargs['code'],
			'comunidad': self.comunidad.id,
		}

		facturacion_masiva.delay(data=request.data, context=context)
		
		return Response(status=status.HTTP_201_CREATED)
