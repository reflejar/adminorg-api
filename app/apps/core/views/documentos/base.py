from datetime import datetime, date
from django.http import Http404
from django.shortcuts import get_object_or_404 
from django.db import transaction

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django_afip.models import (
	DocumentType,
	ReceiptType,
)
from apps.users.permissions import IsComunidadMember, IsAdministrativoUser
from apps.utils.generics import custom_viewsets
from apps.core.serializers import (
	MasivoClienteModelSerializer,
	DestinoClienteModelSerializer,
	OrigenProveedorModelSerializer,
	TesoroModelSerializer,
	AsientoModelSerializer
)
from apps.core.models import (
	Documento,
)
from apps.core.filters import (
	DocumentoFilter
)

class BaseViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Base de Documentos
	"""

	sin_destinatario = False
	filterset_class = DocumentoFilter

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj


	def get_queryset(self):
		try:
			kwargs = {
				'comunidad': self.comunidad,
			}
			if not self.causante in ["caja", "asiento"]:
				kwargs.update({
					'destinatario__naturaleza__nombre': self.causante
				})

			return Documento.objects.filter(**kwargs)
		except:
			raise Http404

	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsAdministrativoUser]
		if self.action in ['update', 'retrieve', 'delete']:
			permissions.append(IsComunidadMember)
		return [p() for p in permissions]


	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		serializer_context.update({
			'causante': self.causante,
			'sin_destinatario': self.sin_destinatario,
		})		
		if "pk" in self.kwargs.keys():
			obj = self.get_object()
			serializer_context['retrieve'] = True
			serializer_context['receipt_type'] = ReceiptType.objects.get(
				description=obj.receipt.receipt_type
			)			
			serializer_context['cuenta'] = obj.destinatario
		else:
			if self.request.method == 'POST':	
				serializer_context['receipt_type'] = ReceiptType.objects.get(
					description=self.request.data['receipt']['receipt_type'] 
				)

		return serializer_context

	def get_fecha(self):
		fecha = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date() if 'end_date' in self.request.GET.keys() else date.today()
		return fecha

	def destroy_valid_disponibilidades(self, obj):

		utilizaciones_disponibilidades = obj.disponibilidades_utilizaciones()
		if utilizaciones_disponibilidades:
			textos = ["{}. ".format(u.receipt) for u in utilizaciones_disponibilidades]
			raise serializers.ValidationError("Primero debe anular los comprobantes: {}".format(''.join(textos)))
		

	def destroy_valid_saldos(self, obj):

		utilizaciones_saldos = obj.a_cuenta_utilizaciones()
		if utilizaciones_saldos:
			textos = ["{}. ".format(u.receipt) for u in utilizaciones_saldos]
			raise serializers.ValidationError("Primero debe anular los comprobantes: {}".format(''.join(textos)))
		

	def destroy_valid_pagos(self, obj):

		pagos = obj.pagos_recibidos()
		if pagos:
			textos = ["{}. ".format(p.receipt) for p in pagos]
			raise serializers.ValidationError("Primero debe anular los comprobantes: {}".format(''.join(textos)))

	def destroy_valid_anulado(self, obj):
		if obj.fecha_anulacion:
			raise serializers.ValidationError("El documento ya se encuentra anulado")
