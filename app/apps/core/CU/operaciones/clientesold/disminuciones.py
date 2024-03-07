from datetime import date
from django.db.models import Max
from django_afip.models import (
	Receipt,
	ReceiptType,
	PointOfSales
)
from rest_framework import serializers

from apps.core.models import (
	Documento, 
	Operacion,
	Cuenta,
	OwnReceipt
)
from apps.utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.cobros = validated_data['cobros']
		self.punto_de_venta = self.comunidad.contribuyente.points_of_sales.get(number=self.receipt.point_of_sales)

		if self.receipt.receipt_type.code == "54":
			self.cajas = validated_data['cajas']
			self.utilizaciones_saldos = validated_data['utilizaciones_saldos']
			self.utilizaciones_disponibilidades = validated_data['utilizaciones_disponibilidades']
		
		elif self.receipt.receipt_type.code in ["13", "53"]:
			self.resultados = validated_data['resultados']

		try:
			self.cuenta_interes = Cuenta.objects.get(comunidad=self.comunidad, taxon__nombre="interes_predeterminado")
		except:
			self.cuenta_interes = None
		try:
			self.cuenta_descuento = Cuenta.objects.get(comunidad=self.comunidad, taxon__nombre="descuento_predeterminado")
		except:
			self.cuenta_descuento = None
		
		self.suma_totales = 0
		self.suma_cobros = 0
		self.suma_descuentos_c = 0
		self.suma_intereses_c = 0
		self.suma_descuentos_x = 0
		self.suma_intereses_x = 0

		self.documentos = {
			'original': self.documento,
			'ncc-automatica': None,
			'ndc-automatica': None,
			'ncx-automatica': None,
			'ndx-automatica': None,	

		}
		self.operaciones = []

	def get_metodo(self, cuenta, naturaleza):
		
		try:
			return cuenta.metodos.get(naturaleza=naturaleza)
		except:
			return


	def hacer_cobros(self):
		""" Realiza las operaciones de cobros de creditos """
		for i in self.cobros:
			self.suma_cobros += i['monto']
			if i['vinculo'].saldo(fecha=self.fecha_operacion) == i['monto']:
				descuento = i['vinculo'].descuento(fecha=self.fecha_operacion)
			else:
				descuento = 0
			interes = i['vinculo'].interes(fecha=self.fecha_operacion)
			if i['monto'] <= interes: # Solo si el pago no supera el interes adeudado, todo el monto del pago se destina a interes.
				interes = i['monto']

			# Creación del descuento.
			if descuento > 0:
				if i['vinculo'].documento.receipt_afip:
					self.suma_descuentos_c += descuento
				else:
					self.suma_descuentos_x += descuento
				operacion_haber_descuento = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de credito
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=-descuento,
					detalle=i['detalle'],
					vinculo=i['vinculo'],
				)
				operacion_haber_descuento.save() # Se guarda directamente este movimiento				

				operacion_debe_descuento = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de credito
					asiento=self.identifier,
					cuenta=self.cuenta_descuento,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=descuento,
					detalle=i['detalle'],
					vinculo=operacion_haber_descuento,
				)
				self.operaciones.append(operacion_debe_descuento)
			

			# Se aumenta la deuda del socio por el interes generado registra imputacion a la cuenta asignada a intereses si el interes es mayor a 0.
			if interes > 0:
				if i['vinculo'].documento.receipt_afip:
					self.suma_intereses_c += interes
				else:
					self.suma_intereses_x += interes
				operacion_debe_interes = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de debito
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=interes,
					detalle=i['detalle'],
					vinculo=i['vinculo'],
				)
				operacion_debe_interes.save() # Se guarda directamente este movimiento

				operacion_haber_interes = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de debito
					asiento=self.identifier,
					cuenta=self.cuenta_interes,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=-interes,
					detalle=i['detalle'],
					vinculo=operacion_debe_interes,
				)
				self.operaciones.append(operacion_haber_interes)	

				operacion_haber_pago_interes = Operacion( # Se paga el interes generado
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento,
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=-interes,
					detalle=i['detalle'],
					vinculo=operacion_debe_interes,
				)
				operacion_haber_pago_interes.save() # Se guarda directamente este movimiento				



			# Solo si el pago supera el interes adeudado, se abona capital.
			# Si existe interes > 0 el pago de capital se ve disminuido por el mismo.
			if i['monto'] > interes:
				monto_capital = i['monto'] - interes
				operacion_haber_credito = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento,
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=i['vinculo'].fecha_indicativa or self.fecha_operacion,
					valor=-monto_capital,
					detalle=i['detalle'],
					vinculo=i['vinculo'],
				)
				self.operaciones.append(operacion_haber_credito)
			
		
	def hacer_cajas(self):
		""" Realiza las operaciones de caja """
		for i in self.cajas:
			self.suma_totales += i['monto']
			operacion_debe_caja = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				fecha_vencimiento=i['fecha_vencimiento'],
				fecha_indicativa=self.fecha_operacion,
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_debe_caja)


	def hacer_utilizaciones(self):
		""" Realiza las operaciones de utilizaciones_saldos y utilizaciones_disponibilidades """
		utilizaciones_totales = self.utilizaciones_saldos + self.utilizaciones_disponibilidades
		for i in utilizaciones_totales:
			self.suma_totales += i['monto']
			operacion_debe_saldo = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=i['vinculo'].cuenta,
				fecha_indicativa=self.fecha_operacion,
				valor=i['monto'],
				detalle=i['detalle'],
				vinculo=i['vinculo'],
			)
			self.operaciones.append(operacion_debe_saldo)


	def hacer_resultados(self):
		""" Realiza las operaciones de la contraparte de los cobros perdonados en las Notas de Credito C manuales """
		for i in self.resultados:
			self.suma_totales += i['monto']
			operacion_debe_resultado = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				fecha_indicativa=i['periodo'] or self.fecha_operacion,
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_debe_resultado)


	def hacer_notas_credito(self):
		"""
			Realiza el Receipt de la nota de credito automatica por los descuentos
			Realiza el documento y la guarda en self.documentos['nc-automatica']
		"""

		if self.suma_descuentos_c > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="13")
			nota_credito_afip = Receipt.objects.create(
					point_of_sales=self.punto_de_venta,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_descuentos_c,
					net_untaxed=0,
					net_taxed=self.suma_descuentos_c,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)				
			self.tratamiento_receipts_derivados(nota_credito_afip)
			nota_credito = OwnReceipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_descuentos_c,
					net_untaxed=0,
					net_taxed=self.suma_descuentos_c,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)
			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_credito,
					receipt_afip=nota_credito_afip,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Credito por Descuento",
				)
			documento.chequear_numeros()
			self.documentos['ncc-automatica'] = documento


		if self.suma_descuentos_x > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="53")
			nota_credito = OwnReceipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_descuentos_x,
					net_untaxed=0,
					net_taxed=self.suma_descuentos_x,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)
			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_credito,
					receipt_afip=None,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Credito por Descuento",
				)
			documento.chequear_numeros()
			self.documentos['ncx-automatica'] = documento


	def hacer_notas_debito(self):
		"""
			Realiza el Receipt de la nota de debito automatica por los intereses
			Realiza el documento y la guarda en self.documentos['nd-automatica']
		"""
		if self.suma_intereses_c > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="12")
			nota_debito_afip = Receipt.objects.create(
					point_of_sales=self.punto_de_venta,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_intereses_c,
					net_untaxed=0,
					net_taxed=self.suma_intereses_c,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)
			self.tratamiento_receipts_derivados(nota_debito)
			nota_debito = OwnReceipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_intereses_c,
					net_untaxed=0,
					net_taxed=self.suma_intereses_c,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)				
			
			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_debito,
					receipt_afip=nota_debito_afip,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Debito por Intereses",
				)
			documento.chequear_numeros()
			self.documentos['ndc-automatica'] = documento

		if self.suma_intereses_x > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="52")
			nota_debito = OwnReceipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_intereses_x,
					net_untaxed=0,
					net_taxed=self.suma_intereses_x,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)				
			
			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_debito,
					receipt_afip=None,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Debito por Intereses",
				)
			documento.chequear_numeros()
			self.documentos['ndx-automatica'] = documento			

	def tratamiento_receipts_derivados(self, receipt_derivado):
		"""
			Valida los documentos derivados del principal en caso de que haya que hacerlo
			Coloca el numero en caso de que no tenga
		"""
		pass
		# if receipt_derivado.receipt_type.code in ["12", "13"]:
		# 	if self.comunidad.contribuyente.certificate: 
		# 		try:
		# 			error = receipt_derivado.validate()
		# 		except:
		# 			error = True
		# 		if error:
		# 			raise serializers.ValidationError('No se pudo validar en AFIP. Vuelve a intentarlo mas tarde')

		# if not receipt_derivado.receipt_number:
		# 	last = Receipt.objects.filter(
		# 		receipt_type=receipt_derivado.receipt_type,
		# 		point_of_sales=receipt_derivado.point_of_sales,
		# 	).aggregate(Max('receipt_number'))['receipt_number__max'] or 0
		# 	receipt_derivado.receipt_number = last + 1
		# 	receipt_derivado.save()
				


	def colocar_documentos(self):
		"""
			Coloca los documentos en cada operacion
		"""

		for i in self.operaciones: # Primero coloca el documento comun a todos
			i.documento = self.documentos['original']

		for i in self.operaciones: # Luego lo modifica en caso de que sea otro
			if (self.documentos['ncc-automatica'] or self.documentos['ncx-automatica']) and i.cuenta == self.cuenta_descuento:
				# Si esta operacion tiene cuenta de descuento
				if i.vinculo.vinculo.documento.receipt_afip: # Si el vinculo del vinculo tiene receipt_afip entonces va C
					i.documento = self.documentos['ncc-automatica']
					i.vinculo.documento = self.documentos['ncc-automatica']
				else: # Sino va X
					i.documento = self.documentos['ncx-automatica']
					i.vinculo.documento = self.documentos['ncx-automatica']
				i.vinculo.save()
			elif (self.documentos['ndc-automatica'] or self.documentos['ndx-automatica']) and i.cuenta == self.cuenta_interes:
				# Si esta operacion tiene cuenta de interes
				if i.vinculo.vinculo.documento.receipt_afip:
					i.documento = self.documentos['ndc-automatica']
					i.vinculo.documento = self.documentos['ndc-automatica']
				else:
					i.documento = self.documentos['ndx-automatica']
					i.vinculo.documento = self.documentos['ndx-automatica']
				i.vinculo.save()


	def hacer_saldo_a_favor(self):
		""" Realiza la operacion de saldo a favor """
		if self.suma_totales > self.suma_cobros:
			operacion_haber_saldo = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=self.documento.destinatario,
				fecha_indicativa=self.fecha_operacion,
				valor=-self.suma_totales + self.suma_cobros,
				detalle="Saldo a favor",
			)
			self.operaciones.append(operacion_haber_saldo)


	def create(self):
		
		self.hacer_cobros()
		
		if self.receipt.receipt_type.code == "54":
			self.hacer_cajas()
			self.hacer_utilizaciones()

		elif self.receipt.receipt_type.code in ["13", "53"]:
			self.hacer_resultados()

		self.hacer_saldo_a_favor()


		# Creacion de nota de debito o de credito automatica
		if self.receipt.receipt_type.code == "54":
			self.hacer_notas_credito()
			self.hacer_notas_debito()

		self.colocar_documentos()

		# bulk_create de las operaciones
		Operacion.objects.bulk_create(self.operaciones)
	
		return Operacion.objects.filter(asiento=self.identifier)


