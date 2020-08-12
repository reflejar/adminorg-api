from datetime import date
from django_afip.models import *
from django.db import models, transaction

from admincu.operative.models import (
	Documento, 
	Operacion,
	Cuenta
)
from admincu.utils.generics.functions import *


class CU:
	
	""" Crea las Operaciones y los Documentos """

	def __init__(self, documento, validated_data):
		self.documento_base = documento
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.receipt_base = validated_data['receipt']
		self.receipt_base.update({
			'receipt_type': ReceiptType.objects.get(code="11"),
			'service_start': self.fecha_operacion,
			'service_end': self.fecha_operacion,
			'expiration_date': self.fecha_operacion,
			'net_untaxed': 0.00,
			'exempt_amount': 0.00,			
			'currency': CurrencyType.objects.get(code="PES")
		})

		self.distribuciones = validated_data['distribuciones']
		self.preconceptos = validated_data['preconceptos']
		self.ingresos_preconceptos = Operacion.objects.filter(vinculo__in=self.preconceptos)

		self.socios = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="cliente")
		self.dominios = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="dominio")


	def preparar_preconceptos(self):
		
		self.preconceptos.update(
				asiento=self.identifier,
				fecha=self.fecha_operacion
			)
		self.ingresos_preconceptos.update(
				asiento=self.identifier,
				fecha=self.fecha_operacion
			)

	def hacer_creditos(self):

		for d in self.distribuciones:
			if d['unidad'] == "socio":
				for s in self.socios:
					if s.vinculaciones.all():
						operacion_debe = Operacion.objects.create(
							comunidad=self.comunidad,
							cuenta=s,
							asiento=self.identifier,
							valor=d['monto'],
							detalle=d['descripcion'],
							fecha=self.documento.fecha_operacion,
							fecha_indicativa=d['periodo'],
							fecha_gracia=credito['fecha_gracia'],
							fecha_vencimiento=credito['fecha_vencimiento'],
						)
						if metodo_interes:
							operacion_debe.metodos.add(metodo_interes)
						if metodo_descuento:
							operacion_debe.metodos.add(metodo_descuento)
						
						operacion_haber = Operacion.objects.create(
							comunidad=self.comunidad,
							cuenta=d['ingreso'],
							asiento=self.identifier,
							valor=d['monto'],
							detalle=d['descripcion'],
							fecha=self.documento.fecha_operacion,
							fecha_indicativa=d['periodo'],
							fecha_gracia=credito['fecha_gracia'],
							fecha_vencimiento=credito['fecha_vencimiento'],
							vinculo=operacion_debe
						)

			else:
				for d in self.dominios:
					if d.propietario() or d.ocupante():
						if d['unidad'] == "dominio":
							monto = d['monto']
						else:
							if d.domicilio.superficie_total:
								monto = d.domicilio.superficie_total * d['monto']
							else:
								monto = 0

						if monto != 0:
							operacion_debe = Operacion.objects.create(
								comunidad=self.comunidad,
								cuenta=d,
								asiento=self.identifier,
								valor=monto,
								detalle=d['descripcion'],
								fecha=self.documento.fecha_operacion,
								fecha_indicativa=d['periodo'],
								fecha_gracia=credito['fecha_gracia'],
								fecha_vencimiento=credito['fecha_vencimiento'],
							)
							if d['ingreso'].interes():
								operacion_debe.metodos.add(d['ingreso'].interes())
							if d['ingreso'].descuento():
								operacion_debe.metodos.add(d['ingreso'].descuento())
							
							operacion_haber = Operacion.objects.create(
								comunidad=self.comunidad,
								cuenta=d['ingreso'],
								asiento=self.identifier,
								valor=d['monto'],
								detalle=d['descripcion'],
								fecha=self.documento.fecha_operacion,
								fecha_indicativa=d['periodo'],
								fecha_gracia=credito['fecha_gracia'],
								fecha_vencimiento=credito['fecha_vencimiento'],
							)

	def hacer_documentos(self):
		self.operaciones = Operacion.objects.filter(asiento=self.identifier)
		for s in self.socios:
			if s.vinculaciones.all():
				operaciones_socio = self.operaciones.filter(cuenta__in=s.grupo)
				total = operaciones_socio.filter(valor__gt=0).aggregate(calculo=models.Sum('valor'))['calculo']
				
				receipt_data = self.receipt_base.copy()
				receipt_data.update({
					'document_type': s.perfil.tipo_documento,
					'document_number': s.perfil.numero_documento,
					'total_amount': total,
					'net_taxed': total,
				})
				receipt = Receipt.objects.create(**receipt_data)
				
				documento = self.documento_base.copy()
				documento.receipt = receipt
				documento.destinatario = destinatario
				documento.descripcion = descripcion
				documento.save()

				operaciones_socio.update(documento=documento)

	@transaction.atomic
	def create(self):
		""" 
			Realiza todas las operaciones desde la configuracion recibida
			Reagrupa todas las operaciones para colocar el destinatario y hacer cada documento

		"""
		# self.hacer_creditos()
		# self.preparar_preconceptos()
		# self.hacer_documentos()

		return Documento.objects.none()