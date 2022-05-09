from datetime import date
from django_afip.models import *
from django.db import models, transaction
from django.db.models import Max

from adminsmart.apps.core.models import (
	Documento, 
	Operacion,
	Cuenta,
	OwnReceipt
)
from adminsmart.apps.utils.generics.functions import *


class CU:
	
	""" Crea las Operaciones y los Documentos """

	def __init__(self, documento, validated_data):
		self.documento_base = documento
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.receipt_base = validated_data['receipt']
		self.receipt_base.update({
			'service_start': self.fecha_operacion,
			'service_end': self.fecha_operacion,
			'expiration_date': self.fecha_operacion,
			'net_untaxed': 0.00,
			'exempt_amount': 0.00,			
			'currency': CurrencyType.objects.get(code="PES")
		})

		self.distribuciones = validated_data['distribuciones']
		self.preconceptos = Operacion.objects.filter(id__in=[x.id for x in validated_data['preconceptos']])
		self.ingresos_preconceptos = Operacion.objects.filter(vinculo__in=self.preconceptos)

		self.socios = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="cliente")
		self.dominios = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre="dominio")
		self.documentos_creados = []


	def preparar_preconceptos(self):
		

		self.preconceptos.update(
				asiento=self.identifier,
				fecha=self.fecha_operacion
			)
		self.ingresos_preconceptos.update(
				asiento=self.identifier,
				fecha=self.fecha_operacion
			)

	def get_metodo(self, cuenta, naturaleza):
		try:
			return cuenta.metodos.get(naturaleza=naturaleza)
		except:
			return
			
	def hacer_creditos(self):

		for d in self.distribuciones:
			metodo_interes = self.get_metodo(cuenta=d['ingreso'], naturaleza='interes')
			metodo_descuento = self.get_metodo(cuenta=d['ingreso'], naturaleza='descuento') 			
			if d['unidad'] == "socio":
				for s in self.socios:
					if s.vinculaciones():
						operacion_debe = Operacion.objects.create(
							comunidad=self.comunidad,
							cuenta=s,
							asiento=self.identifier,
							valor=d['monto'],
							fecha=self.documento_base.fecha_operacion,
							fecha_indicativa=self.documento_base.fecha_operacion,
							fecha_gracia=d['fecha_gracia'],
							fecha_vencimiento=d['fecha_vencimiento'],
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
							fecha=self.documento_base.fecha_operacion,
							fecha_indicativa=self.documento_base.fecha_operacion,
							fecha_gracia=d['fecha_gracia'],
							fecha_vencimiento=d['fecha_vencimiento'],
							vinculo=operacion_debe
						)

			else:
				for dominio in self.dominios:
					if dominio.propietario() or dominio.inquilino():
						if d['unidad'] == "dominio":
							monto = d['monto']
						else:
							if dominio.domicilio.superficie_total:
								monto = d.domicilio.superficie_total * d['monto']
							else:
								monto = 0

						if monto != 0:
							operacion_debe = Operacion.objects.create(
								comunidad=self.comunidad,
								cuenta=dominio,
								asiento=self.identifier,
								valor=monto,
								fecha=self.documento_base.fecha_operacion,
								fecha_indicativa=self.documento_base.fecha_operacion,
								fecha_gracia=d['fecha_gracia'],
								fecha_vencimiento=d['fecha_vencimiento'],
							)
							if d['ingreso'].interes():
								operacion_debe.metodos.add(d['ingreso'].interes())
							if d['ingreso'].descuento():
								operacion_debe.metodos.add(d['ingreso'].descuento())
							
							operacion_haber = Operacion.objects.create(
								comunidad=self.comunidad,
								cuenta=d['ingreso'],
								asiento=self.identifier,
								valor=-monto,
								fecha=self.documento_base.fecha_operacion,
								fecha_indicativa=self.documento_base.fecha_operacion,
								fecha_gracia=d['fecha_gracia'],
								fecha_vencimiento=d['fecha_vencimiento'],
								vinculo=operacion_debe
							)

	def hacer_documentos(self):
		self.operaciones = Operacion.objects.filter(asiento=self.identifier)
		for s in self.socios:
			# if s.vinculaciones():
			operaciones_socio = self.operaciones.filter(cuenta__in=s.grupo)
			total = operaciones_socio.filter(valor__gt=0).aggregate(calculo=models.Sum('valor'))['calculo']
			if total:
				receipt_data = self.receipt_base.copy()
				receipt_data.update({
					'receipt_type': ReceiptType.objects.get(description=receipt_data['receipt_type']),
					'document_type': s.perfil.tipo_documento,
					'document_number': s.perfil.numero_documento,
					'total_amount': total,
					'net_taxed': total,
				})
				receipt = OwnReceipt.objects.create(**receipt_data)

				receipt_afip = None
				# if receipt_data['receipt_type'].code == "11":
				# 	receipt_afip = Receipt.objects.create(**receipt_data)
				# 	try:
				# 		error = receipt_afip.validate()
				# 		receipt.receipt_number = receipt_afip.receipt_number
				# 	except:
				# 		error = True	
				
				documento = self.documento_base
				documento.pk = None
				documento.receipt = receipt
				documento.receipt_afip = receipt_afip
				documento.destinatario = s
				documento.save()
				documento.chequear_numeros()

				operaciones_socio.update(documento=documento)
				for o in operaciones_socio:
					o.vinculos.update(documento=documento)
				self.documentos_creados.append(documento.id)


	@transaction.atomic
	def create(self):
		""" 
			Realiza todas las operaciones desde la configuracion recibida
			Reagrupa todas las operaciones para colocar el destinatario y hacer cada documento

		"""
		self.hacer_creditos()
		self.preparar_preconceptos()
		self.hacer_documentos()

		return self.documentos_creados