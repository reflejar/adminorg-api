from __future__ import unicode_literals
import json
import base64
from functools import reduce
from datetime import date

from django.db.models import Max
from django.db import models
from django.apps import apps
from django_afip.models import (
	Receipt,
	ReceiptType
)
from django_afip.pdf import ReceiptBarcodeGenerator

from apps.utils.models import BaseModel
from apps.core.models.own_receipt import OwnReceipt
from apps.files.models import PDF


class Documento(BaseModel):
	"""
		Modelo de Documentos
		Representa TODOS los documentos posibles de la entidad
		Todas las operaciones tienen documento, si no la tienen el documento se llama Asiento Contable
		attr receipt es para realizar envio a afip (solo clientes)
		attr own_receipt se establece SIEMPRE. (Copia la data de receipt en el caso de cliente, en los otros casos se establece directamente aqui) 
	"""

	receipt_afip = models.ForeignKey(Receipt, blank=True, null=True, on_delete=models.PROTECT, related_name="documentos") # Solo para "clientes"
	receipt = models.ForeignKey(OwnReceipt, blank=True, null=True, on_delete=models.PROTECT, related_name="documentos") # Todos
	destinatario = models.ForeignKey("operative.Cuenta", blank=True, null=True, on_delete=models.SET_NULL, related_name="documentos")
	pdf = models.ForeignKey("files.PDF", blank=True, null=True, on_delete=models.SET_NULL, related_name="documentos")
	descripcion = models.CharField(max_length=150, blank=True, null=True)
	fecha_operacion = models.DateField()
	fecha_anulacion = models.DateField(blank=True, null=True)

	def __str__(self):
		nombre = str(self.receipt)
		return nombre

	def nombre(self):
		return str(self.receipt)

	def get_model(self, nombre):
		return apps.get_model('operative', nombre)

	def portador(self):
		return str(self.destinatario)

	def tipo(self):
		return str(self.receipt.receipt_type)

	def numero(self):
		return str(self.receipt.formatted_number)		

	# Funciones Serializadoras
	def creditos(self):
		"""
			Clientes: Factura C, X y Nota de Debito C, X manuales 
		"""		
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			cuenta__in=self.destinatario.grupo,
			# vinculo__isnull=True,
			cuenta__naturaleza__nombre__in=['cliente', 'dominio'],
			valor__gt=0,
		)		

	def debitos(self):
		"""
			Proveedores: Documentos de debitos (No OP ni Notas de Credito)
		"""
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			vinculo__isnull=True,
			cuenta__naturaleza__nombre__in=["caja", "gasto", "bien_de_cambio", "bien_de_uso"],
			valor__gt=0,
		).exclude(descripcion="ANULACION")

	def cargas(self):
		"""
			Tesoreria: Documento tipo Transferencia
		"""
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			documento__destinatario__isnull=True,
			vinculo__isnull=True,
			valor__gt=0,
		).exclude(descripcion="ANULACION")

	def pagos(self):
		"""
			Proveedores: Documentos de disminuciones (OP y Notas de Credito)
		"""		
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			vinculo__isnull=False,
			cuenta=self.destinatario,
			valor__gt=0,
		).exclude(descripcion="ANULACION")

	def cobros(self):
		"""
			Clientes: Recibo X y Nota de Credito C manuales 
		"""
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			vinculo__isnull=False,
			cuenta__naturaleza__nombre__in=['cliente', 'dominio'],
			valor__lt=0,
		).exclude(descripcion="ANULACION")

	def resultados(self):
		"""
			Clientes: Notas de Credito C
			Proveedores: Todas las Notas de Credito
		"""		
		identifier = self.operaciones.first().asiento
		kwargs = {
			'asiento': identifier,
			'vinculo__isnull': True,
			'cuenta__naturaleza__nombre__in': ['ingreso', 'gasto'],
		}
		if self.destinatario.naturaleza.nombre == "cliente":
			kwargs.update({'valor__gt': 0})
		elif self.destinatario.naturaleza.nombre == "proveedor":
			kwargs.update({'valor__lt': 0})


		return self.get_model('Operacion').objects.filter(**kwargs)

	def cajas(self):
		"""
			Clientes: Recibo X
			Proveedores: OP
		"""		
		identifier = self.operaciones.first().asiento
		kwargs = {
			'asiento': identifier,
			'vinculo__isnull': True,
			'cuenta__naturaleza__nombre': 'caja',
		}
		if self.destinatario:

			if self.destinatario.naturaleza.nombre == "cliente":
				kwargs.update({
					'valor__gt': 0,
				})
			elif self.destinatario.naturaleza.nombre == "proveedor":
				kwargs.update({
					'valor__lt': 0,
				})
		else:
			if self.receipt.receipt_type.code == "303":
				kwargs.update({
					'valor__lt': 0,
				})

		result = self.get_model('Operacion').objects.filter(**kwargs).exclude(cuenta__naturaleza__nombre="stockeable")
		return result.exclude(descripcion="ANULACION")

	def utilizaciones_saldos(self):
		"""
			Clientes: Recibo X
			Proveedores: OP
		"""		
		identifier = self.operaciones.first().asiento
		kwargs = {
			'asiento': identifier,
			'vinculo__isnull': False,
		}
		if self.destinatario.naturaleza.nombre == "cliente":
			kwargs.update({
				'cuenta__naturaleza__nombre__in': ['cliente'],
				'valor__gt': 0,
				'documento__receipt__receipt_type': self.receipt.receipt_type # Las utilizaciones de saldo solo se tienen documento tipo Recibo X en clientes
			})
		elif self.destinatario.naturaleza.nombre == "proveedor":
			kwargs.update({
				'cuenta': self.destinatario,
				'valor__lt': 0,
			})
		return self.get_model('Operacion').objects.filter(**kwargs).exclude(descripcion="ANULACION")

	def a_cuenta(self):
		"""
			Clientes: Recibo X
			Proveedores: OP
		"""		
		identifier = self.operaciones.first().asiento
		kwargs = {
			'asiento': identifier,
			'vinculo__isnull': True,
		}
		if self.destinatario.naturaleza.nombre == "cliente":
			kwargs.update({
				'cuenta__naturaleza__nombre': 'cliente',
				'valor__lt': 0,
			})
		elif self.destinatario.naturaleza.nombre == "proveedor":
			kwargs.update({
				'cuenta': self.destinatario,
				'valor__gt': 0,
			})

		return self.get_model('Operacion').objects.filter(**kwargs).exclude(descripcion="ANULACION")

	def a_cuenta_utilizaciones(self):
		""" Esto retorna los documentos de los pagos si es que el saldo es distinto al valor original """
		a_cuenta = self.a_cuenta().first()
		if a_cuenta:
			documentos = []

			if a_cuenta.saldo() != a_cuenta.monto:
				for p in a_cuenta.pagos_capital():
					documentos.append(p.documento)
				return set(documentos)

		return 		

	def utilizaciones_disponibilidades(self):
		"""
			Clientes: Recibo X
			Proveedores: Todo
		"""		
		identifier = self.operaciones.first().asiento
		kwargs = {
			'asiento': identifier,
			'vinculo__isnull': False,
			'cuenta__naturaleza__nombre': 'caja',
			'cuenta__taxon__nombre': 'stockeable',
		}
		return self.get_model('Operacion').objects.filter(**kwargs).exclude(descripcion="ANULACION")

	def disponibilidades_utilizaciones(self):
		""" Esto retorna los documentos de las utilizaciones de las disponibilidades creadas si es que el saldo es distinto al valor original """
		disponibilidades = self.cajas().filter(cuenta__taxon__nombre="stockeable")
		if disponibilidades:
			documentos = []
			for d in disponibilidades:
				if d.saldo() != d.monto:
					for p in d.pagos_capital():
						documentos.append(p.documento)
					return set(documentos)

		return 		

	def deuda(self):
		"""
			Proveedores: solo operaciones de debitos que no sean Ordenes de Pago
		"""		
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			vinculo__isnull=True,
			cuenta=self.destinatario,
			valor__lt=0,
		).exclude(documento__receipt__receipt_type__code="302")

	def pagos_recibidos(self):
		""" Esto retorna el ultimo pago si es que el saldo es distinto al valor original """
		identifier = self.operaciones.first().asiento	
		deudas_generadas = self.get_model('Operacion').objects.filter(
			asiento=identifier,
			cuenta__naturaleza__nombre__in=["cliente", "dominio", "proveedor"], 
			vinculo__isnull=True
		)
		if deudas_generadas:
			documentos = []

			for d in deudas_generadas:
				if d.saldo() != d.monto:
					for p in d.pagos_capital():
						documentos.append(p.documento)
			return set(documentos)
		return 
		
	def debe(self):
		""" Esto retorna el todas las operaciones que van en el debe """
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			valor__gt=0,
		).exclude(descripcion="ANULACION")
	
	def haber(self):
		""" Esto retorna el todas las operaciones que van en el haber """
		identifier = self.operaciones.first().asiento
		return self.get_model('Operacion').objects.filter(
			asiento=identifier,
			valor__lt=0,
		).exclude(descripcion="ANULACION")

	def plataforma(self):
		return self.cobros_plataforma.first()


	def anulacion_documentos(self, documentos_relacionados):
		"""
			Genera los documentos necesarios de anulacion de los automaticos
			ANOTACION TEMPORAL: Como solo se está usando Facturas tipo X
			No está generando las nc por nd ni viceversa... solo le pone fecha de anulacion
		"""
		documentos = {
			'original': self,
			'nc-automatica': None,
			'nd-automatica': None,
			'nc-automatica-anulacion': None,
			'nd-automatica-anulacion': None
		}		
		if len(documentos_relacionados) > 1:
			for d in documentos_relacionados:
				if d != self:
					d.fecha_anulacion = self.fecha_anulacion
					d.save()

					# if d.receipt.receipt_type.code in ["13", "53"]:
					# 	documentos['nc-automatica'] = d
					# 	nota_debito = d
					# 	nota_debito.pk = None
					# 	receipt = nota_debito.receipt
					# 	receipt.pk = None
					# 	receipt.receipt_number = None
					# 	receipt_type_code = "12" if d.receipt.receipt_type.code == "13" else "52"
					# 	receipt.receipt_type = ReceiptType.objects.get(code=receipt_type_code)
					# 	receipt.issued_date = date.today()
					# 	receipt.save()
					# 	try:
					# 		error = receipt.validate()
					# 	except:
					# 		error = True
					# 	if error:
					# 		raise serializers.ValidationError('No se pudo validar en AFIP. Vuelve a intentarlo mas tarde')
					# 	nota_debito.receipt = receipt
					# 	nota_debito.save()
					# 	documentos['nd-automatica-anulacion'] = nota_debito
					# elif d.receipt.receipt_type.code in ["12", "52"]:
					# 	documentos['nd-automatica'] = d
					# 	nota_credito = d
					# 	nota_credito.pk = None
					# 	receipt = nota_credito.receipt
					# 	receipt.pk = None
					# 	receipt.receipt_number = None	
					# 	receipt_type_code = "13" if d.receipt.receipt_type.code == "12" else "53"					
					# 	receipt.receipt_type = ReceiptType.objects.get(code=receipt_type_code)
					# 	receipt.issued_date = date.today()
					# 	receipt.save()
					# 	try:
					# 		error = receipt.validate()
					# 	except:
					# 		raise serializers.ValidationError('No se pudo validar en AFIP. Vuelve a intentarlo mas tarde')
					# 	nota_credito.receipt = receipt
					# 	nota_credito.save()
					# 	documentos['nd-automatica-anulacion'] = nota_credito

		return documentos

	def anular(self, fecha=None):
		fecha = fecha if fecha else date.today()
		""" Esto duplica las operaciones pero reversadas y con la fecha recibida """
		fecha = self.fecha_operacion # Como react no esta trayendo la fecha deseada por el administrativo, hacemos que impacte el mismo dia de la realizacion del documento
		self.fecha_anulacion = fecha # Logica bien hecha... hay que hacer que react envie la fecha
		self.save()
		self.hacer_pdf()
		identifier = self.operaciones.first().asiento
		operaciones = self.get_model('Operacion').objects.filter(asiento=identifier)
		documentos_generados = set([o.documento for o in operaciones])
		documentos = self.anulacion_documentos(documentos_generados)


		for i in operaciones:
			id_i = int(i.id)
			i.pk = None
			i.valor = -i.valor
			i.fecha = fecha
			i.descripcion = "ANULACION"
			# if i.documento != self:
			# 	if i.documento.receipt.receipt_type.code in ["12", "52"]:
			# 		i.documento = documentos['nc-automatica-anulacion']
			# 	elif i.documento.receipt.receipt_type.code in ["13", "53"]:
			# 		i.documento = documentos['nd-automatica-anulacion']
			i.save()

	def eliminar_operaciones(self):
		identifier = self.operaciones.first().asiento
		operaciones = self.get_model('Operacion').objects.filter(asiento=identifier)	
		operaciones.delete()

	def eliminar(self):
		""" Esto UNICAMENTE DEUDAS CON PROVEEDORES """
		self.eliminar_operaciones()
		receipt = self.receipt
		self.receipt = None
		self.save()
		receipt.delete()
		self.delete()

	def chequear_numeros(self):
		if not self.receipt.receipt_number:
			if self.receipt_afip:
				self.receipt.receipt_number = self.receipt_afip.receipt_number
			else:
				last = Documento.objects.filter(
					comunidad=self.comunidad,
					receipt__receipt_type=self.receipt.receipt_type,
					receipt__point_of_sales=self.receipt.point_of_sales,
					destinatario__naturaleza=self.destinatario.naturaleza if self.destinatario else None
				).aggregate(Max('receipt__receipt_number'))['receipt__receipt_number__max'] or 0

				self.receipt.receipt_number = last + 1
			self.receipt.save()		

	@property
	def causante(self):
		if self.destinatario:
			return self.destinatario.naturaleza.nombre
		if self.receipt.receipt_type.code == "303":
			return "caja"
		if self.receipt.receipt_type.code == "400":
			return "asiento"

	# @property
	# def total(self):
	# 	return sum([o.valor for o in self.operaciones.all() if o.cuenta in self.destinatario.grupo])

	# def vinculos(self):
	# 	identifier = self.operaciones.first().asiento
	# 	return self.get_model('Operacion').objects.filter(
	# 		vinculos__in=self.get_model('Operacion').objects.filter(
	# 			asiento=identifier
	# 		)
	# 	)

	def generate_context_pdf(self):
		
		def fillna(dispatcher):
			return str(dispatcher) if dispatcher else ''

		header_fields = {
			'DOC_TIPO': fillna(self.receipt.receipt_type),
			'DOC_NUM': fillna(self.receipt.formatted_number),
			'DOC_CODIGO': fillna(self.receipt.receipt_type.code),
			'DOC_FECHA': fillna(self.receipt.issued_date.strftime("%d/%m/%Y")),
			'DOC_TOTAL': fillna(self.receipt.total_amount),

			'COMUNIDAD_LOGO': fillna(self.comunidad.contribuyente.extras.logo.url if self.comunidad.contribuyente.extras else None),
			'COMUNIDAD_NOMBRE': fillna(self.comunidad),
			'COMUNIDAD_DOMICILIO': fillna(self.comunidad.domicilio),
			'COMUNIDAD_CUIT': fillna(self.comunidad.contribuyente.cuit),
			'COMUNIDAD_ACTIVIDAD': fillna(self.comunidad.contribuyente.active_since.strftime("%d/%m/%Y")),
			
			'TITULAR_NOMBRE': fillna(self.destinatario),
			'TITULAR_DOC_TIPO': fillna(self.destinatario.perfil.tipo_documento if self.destinatario else None),
			'TITULAR_DOC_NUM': fillna(self.destinatario.perfil.numero_documento if self.destinatario else None),

			'ANULACION': fillna(self.fecha_anulacion.strftime("%d/%m/%Y") if self.fecha_anulacion else None),
			'FECHA_OP': fillna(self.fecha_operacion.strftime("%d/%m/%Y") if self.fecha_operacion else None),
			'DESCRIPCION': fillna(self.descripcion),
		}

		
		fields_operacion = {
			'cuenta': 'CUENTA',
			'concepto': 'CONCEPTO',
			'periodo': 'PERIODO',
			'monto': 'MONTO',
			'valor': 'VALOR',
			'detalle': "DETALLE",
			'vinculo.documento.receipt.receipt_type': "VINCULO_DOC_TIPO",
			'vinculo.documento.receipt.formatted_number': "VINCULO_DOC_NUM",
			'documento.receipt.receipt_type': 'DOC_TIPO'
		}
		content_fields = {
			'CREDITOS': [],
			'COBROS': [],
			'A_CUENTA': [],
			'PAGOS': [],
			'UTILIZACIONES_SALDOS': [],
			'UTILIZACIONES_DISPONIBILIDADES': [],
			'CAJAS': [],
			'CARGAS': [],
			'RETENCIONES': []
		}
		for key in content_fields.keys():
			list_objects = []
			try:
				for op in getattr(self, key.lower())():
					new_obj = {}
					for f in fields_operacion.keys():
						if "." in f:
							try:
								dispatcher = reduce(getattr, f.split("."), op)
							except:
								pass
						else:
							try:
								dispatcher = getattr(op, f, None)
							except:
								pass
						if callable(dispatcher):
							dispatcher = dispatcher()
						new_obj[fields_operacion[f]] = fillna(dispatcher)
					list_objects.append(new_obj)

				content_fields[key] = list_objects
			except:
				pass
		result = {**header_fields, **content_fields}
		
		return json.dumps(result)		

	# Funciones Operativas
	def hacer_pdf(self):
		
		if self.pdf:
			self.pdf.remove()
			self.pdf.delete()		

		if self.receipt.receipt_type.code == "400":
			return 

		if self.destinatario:
			if self.destinatario.naturaleza.nombre == "proveedor" and self.receipt.receipt_type.code != "301":
				return 			

			# if self.destinatario.naturaleza.nombre == "cliente" and self.receipt.receipt_type.code in ['11', '12', '13']:
			# 	generator = ReceiptBarcodeGenerator(self.receipt_afip)
			# 	barcode = base64.b64encode(generator.generate_barcode()).decode("utf-8")

		self.pdf = PDF.objects.create(
				comunidad=self.comunidad,
				template='pdfs/{}.html'.format(self.receipt.receipt_type.code),
				context=self.generate_context_pdf()
			)
		self.save()

		
