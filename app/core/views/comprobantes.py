from datetime import datetime, date
from django.http import Http404, HttpResponse
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
from users.permissions import IsComunidadMember, IsAdministrativoUser
from utils.generics import custom_viewsets
from core.serializers.comprobante import ComprobanteModelSerializer

from core.models import (
	Comprobante,
	Cuenta
)
from core.filters import (
	ComprobanteFilter
)

class ComprobantesViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Base de Comprobantes
	"""

	sin_destinatario = False
	filterset_class = ComprobanteFilter
	serializer_class = ComprobanteModelSerializer


	def retrieve(self, request, pk=None, **kwargs):
		if 'pdf' in request.GET.keys():
			obj = self.get_object()
			pdf = obj.pdf.serve()
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = f'filename="{obj}.pdf"'
			return response
		return super().retrieve(request, pk, **kwargs)

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj


	def get_queryset(self):
		try:
			return Comprobante.objects.filter(comunidad=self.comunidad)
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
		if "pk" in self.kwargs.keys():
			obj = self.get_object()
			serializer_context['retrieve'] = True
			serializer_context['receipt_type'] = ReceiptType.objects.get(
				description=obj.receipt.receipt_type
			)
			serializer_context['cuenta'] = obj.destinatario
			serializer_context['causante'] = obj.destinatario.naturaleza.nombre
		else:
			if self.request.method == 'GET':
				serializer_context['causante'] = self.request.GET['modulo']
			if self.request.method == 'POST':	
				serializer_context['receipt_type'] = ReceiptType.objects.get(
					description=self.request.data['receipt']['receipt_type']
				)
				serializer_context['cuenta'] = Cuenta.objects.get(id=self.request.data['destinatario'])
				serializer_context['causante'] = self.request.data['modulo']
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
			raise serializers.ValidationError("El comprobante ya se encuentra anulado")

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		# response.status_text = "¡Comprobante realizado con éxito!"
		return response 
