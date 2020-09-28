from datetime import date
from django.db.models import Max
from django_afip.models import (
	Receipt,
	ReceiptType
)
from rest_framework import serializers

from admincu.operative.models import (
	Documento, 
	Operacion,
	Cuenta
)
from admincu.utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.cobros = validated_data['cobros']

		if self.receipt.receipt_type.code == "54":
			self.condonacion = validated_data['condonacion']
			self.cajas = validated_data['cajas']
			self.utilizaciones_saldos = validated_data['utilizaciones_saldos']
			self.utilizaciones_disponibilidades = validated_data['utilizaciones_disponibilidades']
		
		elif self.receipt.receipt_type.code in ["13", "53"]:
			self.condonacion = True
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
		self.suma_descuentos = 0
		self.suma_intereses = 0

		self.documentos = {
			'original': self.documento,
			'nc-automatica': None,
			'nd-automatica': None			
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
			if not self.condonacion:
				if i['vinculo'].saldo(fecha=self.fecha_operacion) == i['monto']:
					descuento = i['vinculo'].descuento(fecha=self.fecha_operacion)
				else:
					descuento = 0
				interes = i['vinculo'].interes(fecha=self.fecha_operacion)
				if i['monto'] <= interes: # Solo si el pago no supera el interes adeudado, todo el monto del pago se destina a interes.
					interes = i['monto']
			else:
				descuento = 0
				interes = 0

			# Creación del descuento.
			if descuento > 0:
				self.suma_descuentos += descuento
				operacion_haber_descuento = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de credito
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
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
					valor=descuento,
					detalle=i['detalle'],
					vinculo=operacion_haber_descuento,
				)
				self.operaciones.append(operacion_debe_descuento)
			

			# Se aumenta la deuda del socio por el interes generado registra imputacion a la cuenta asignada a intereses si el interes es mayor a 0.
			if interes > 0:
				self.suma_intereses += interes
				operacion_debe_interes = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento, # Luego se le cambia el documento cuando se hace la nota de debito
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=self.fecha_operacion,
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
					valor=-interes,
					detalle=i['detalle'],
					vinculo=operacion_debe_interes,
				)
				self.operaciones.append(operacion_haber_interes)	



			# Solo si el pago supera el interes adeudado, se abona capital.
			# Si existe interes > 0 el pago de capital se ve disminuido por el mismo.
			if i['monto'] > interes:
				operacion_haber_credito = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento,
					asiento=self.identifier,
					cuenta=i['vinculo'].cuenta,
					fecha_indicativa=i['vinculo'].fecha_indicativa,
					valor=-i['monto'],
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
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_debe_resultado)


	def hacer_nota_credito(self):
		"""
			Realiza el Receipt de la nota de credito automatica por los descuentos
			Realiza el documento y la guarda en self.documentos['nc-automatica']
		"""

		if self.suma_descuentos > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="13")
			nota_credito = Receipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_descuentos,
					net_untaxed=0,
					net_taxed=self.suma_descuentos,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)
			self.tratamiento_receipts_derivados(nota_credito)

			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_credito,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Credito por Descuento",
				)
			self.documentos['nc-automatica'] = documento


	def hacer_nota_debito(self):
		"""
			Realiza el Receipt de la nota de debito automatica por los intereses
			Realiza el documento y la guarda en self.documentos['nd-automatica']
		"""
		if self.suma_intereses > 0:
			today = date.today()
			receipt_type = ReceiptType.objects.get(code="12")
			nota_debito = Receipt.objects.create(
					point_of_sales=self.receipt.point_of_sales,
					receipt_type=receipt_type,
					concept=self.receipt.concept,
					document_type=self.receipt.document_type,
					document_number=self.receipt.document_number,
					issued_date=today,
					total_amount=self.suma_intereses,
					net_untaxed=0,
					net_taxed=self.suma_intereses,
					exempt_amount=0,
					service_start=today,
					service_end=today,
					expiration_date=today,
					currency=self.receipt.currency,
				)

			self.tratamiento_receipts_derivados(nota_debito)
			
			documento = Documento.objects.create(
					comunidad=self.comunidad,
					receipt=nota_debito,
					destinatario=self.documento.destinatario,
					fecha_operacion=self.documento.fecha_operacion,
					descripcion="Nota de Debito por Intereses",
				)
			self.documentos['nd-automatica'] = documento

	def tratamiento_receipts_derivados(self, receipt_derivado):
		"""
			Valida los documentos derivados del principal en caso de que haya que hacerlo
			Coloca el numero en caso de que no tenga
		"""
		# if receipt_derivado.receipt_type.code in ["12", "13"]:
		# 	if self.comunidad.contribuyente.certificate: 
		# 		try:
		# 			error = receipt_derivado.validate()
		# 		except:
		# 			error = True
		# 		if error:
		# 			raise serializers.ValidationError('No se pudo validar en AFIP. Vuelve a intentarlo mas tarde')

		if not receipt_derivado.receipt_number:
			last = Receipt.objects.filter(
				receipt_type=receipt_derivado.receipt_type,
				point_of_sales=receipt_derivado.point_of_sales,
			).aggregate(Max('receipt_number'))['receipt_number__max'] or 0
			receipt_derivado.receipt_number = last + 1
			receipt_derivado.save()
				


	def colocar_documentos(self):
		"""
			Coloca los documentos en cada operacion
		"""

		for i in self.operaciones: # Primero coloca el documento comun a todos
			i.documento = self.documentos['original']

		for i in self.operaciones: # Luego lo modifica en caso de que sea otro
			if self.documentos['nc-automatica'] and i.cuenta == self.cuenta_descuento:
				i.documento = self.documentos['nc-automatica']
				i.vinculo.documento = self.documentos['nc-automatica']
				i.vinculo.save()
			elif self.documentos['nd-automatica'] and i.cuenta == self.cuenta_interes:
				i.documento = self.documentos['nd-automatica']
				i.vinculo.documento = self.documentos['nd-automatica']
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
				valor=-self.suma_totales + self.suma_cobros,
				detalle="Saldo a favor",
			)
			self.operaciones.append(operacion_haber_saldo)


	def create(self):
		
		self.hacer_cobros()
		
		if self.receipt.receipt_type.code == "54":
			self.hacer_cajas()
			self.hacer_utilizaciones()

		elif self.receipt.receipt_type.code == "13":
			self.hacer_resultados()

		self.hacer_saldo_a_favor()


		# Creacion de nota de debito o de credito automatica
		if self.receipt.receipt_type.code == "54":
			self.hacer_nota_credito()
			self.hacer_nota_debito()

		self.colocar_documentos()

		# bulk_create de las operaciones
		Operacion.objects.bulk_create(self.operaciones)
	
		return Operacion.objects.filter(asiento=self.identifier)


