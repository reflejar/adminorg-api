import datetime
import re
from datetime import datetime

from django.conf import settings
from .models import *

class Exp:
	"""
		Exportador/Importador ExP class, generador de barcode numerico.
	"""

	clientes = set(list(Account.objects.all().values_list('app_code', flat=True)))
	fecha_archivo = datetime.now()

	# Funciones de importacion
	def exp_import(self):
		''' Importador de cobros Exp.'''
		for cliente in self.clientes:
			self.codigo_cliente = cliente
			self.write_db()


	def write_db(self):
		'''Escribe database con datos provistos por txt de exp'''
		listOfLines = []
		nombre = "{}_RD{}.txt".format(str(self.codigo_cliente), self.fecha_archivo.strftime('%Y%m%d'))
		with open ("{}/{}".format(settings.MEDIA_ROOT ,nombre), "r") as myfile:
			for line in myfile:
				listOfLines.append(line.strip())
		listOfLines.pop(0)
		listOfLines.pop()
		listOfCobrosExp = []
		for c in listOfLines:
			listOfCobrosExp.append(Payment(
				codigo_consorcio = self.formato_imp(c[1:5], 'int'),
				unidad_funcional = self.formato_imp(c[5:10], 'int'),
				fecha_cobro = self.formato_imp(c[10:18], 'date'),
				importe_cobrado = self.formato_imp(c[18:29], 'float'),
				comision_plataforma = self.formato_imp(c[29:40], 'float'),
				neto_a_depositar = self.formato_imp(c[40:51], 'float'),
				canal_de_pago = c[51:],
			))
		Payment.objects.bulk_create(listOfCobrosExp)


	def formato_imp(self, val, tipo):
		''' Conversor al formato importacion. Recibe un str y retorna un valor admitido en el modelo. '''
		if tipo == 'float':
			x = val[:9]
			y = val[9:]
			output = float(x + '.' + y)
		if tipo == 'int':
			output = int(val)
		if tipo == 'date':
			output = datetime.datetime.strptime(val, '%Y%m%d').date()
		return output



	# Funciones de exportacion
	def exp_export(self):
		''' Inicializa la clase para crear un acrchivo txt por cliente de Exp.'''
		for cliente in self.clientes:
			self.queryset = Factura.objects.filter(id__gt=3457, consorcio__exp__codigo_exp=cliente, exp__inf_deuda=False)
			if self.queryset:
				self.codigo_cliente = cliente
				self.dato_interno = self.queryset.first().consorcio.exp.first().di_exp
				self.write_txt()


	def write_txt(self):
		''' Crea un archivo txt y escribe una linea por elemento en la lista de registros.'''
		data = self.hacer_data_exp()
		nombre = 'DI_{}_{}.txt'.format(str(self.codigo_cliente), self.fecha_archivo.strftime('%Y%m%d%H%M%S'))
		file_export = open("/home/agustin/Documentos/Proyectos/adminsmart1.0/media/exp/{}".format(nombre), "w")
		for i in data:
			file_export.write(i + os.linesep)
		file_export.close()


	def hacer_data_exp(self):
		''' Concatena header, detalle y trailer. Retorna una lista con un elemento por registro.'''
		data = []
		data.append(self.hacer_header())
		for i in self.hacer_detalle():
			data.append(i)
		data.append(self.hacer_trailer())
		return data


	def hacer_header(self):
		''' Generador de header. Retorna un str.'''
		data_header = [
			self.formato_exp('int', 1, 1),
			self.formato_exp('int', 4, self.codigo_cliente),
			self.formato_exp('int', 14, self.fecha_archivo.strftime('%Y%m%d%H%M%S')),
		]
		return ''.join(data_header)


	def hacer_detalle(self):
		''' Generador de detalle. Retorna una lista de str. Ademas genera self.total_1er_venc y self.total_2do_venc.'''
		data_detalle = []
		self.total_1er_venc = 0
		self.total_2do_venc = 0
		for c in self.queryset:

			try: # Parche necesario porque en la base de dato existen socios sin usuario vinculado, no deberia corresponder en el nuevo sistema.
				email = c.socio.usuarios.first().email # Revisar, aveces manda 2 emails porque hay usuarios que tienen 2 emails cargados ejemplo (mendez mena)
			except:
				email = None

			vinculo = c.exp.first()

			fecha1 = c.expensas_pagas(0)
			fecha2 = c.expensas_pagas(1)
			saldo1 = c.saldo(fecha1)
			saldo2 = c.saldo(fecha2)

			dato = [
				self.formato_exp('int', 1, 5),
				self.formato_exp('int', 4, c.consorcio.id),
				self.formato_exp('int', 5, c.socio.id),
				self.formato_exp('char', 20, c.receipt.issued_date),
				self.formato_exp('char', 40, c.socio),
				self.formato_exp('char', 15, c.socio.domicilio),
				self.formato_exp('char', 40, email),
				self.formato_exp('date', 8, fecha1, '%Y%m%d'),
				self.formato_exp('float', 11, saldo1),
				self.formato_exp('date', 8, fecha2, '%Y%m%d'),
				self.formato_exp('float', 11, saldo2),
				self.formato_exp('int', 14, vinculo.cpe),
				self.formato_exp('int', 56, vinculo.barcode),
			]
			string = ''.join(dato)
			data_detalle.append(string)
			vinculo.inf_deuda = True
			vinculo.save()
			self.total_1er_venc = self.total_1er_venc + saldo1
			self.total_2do_venc = self.total_2do_venc + saldo2
		return data_detalle


	def hacer_trailer(self):
		''' Generador de detale. Retorna un str.'''
		data_trailer = []
		data_trailer.extend((
			self.formato_exp('int', 1, 9),
			self.formato_exp('int', 4, self.codigo_cliente),
			self.formato_exp('int', 14, self.fecha_archivo.strftime('%Y%m%d%H%M%S')),
			self.formato_exp('int', 6, self.queryset.count()),
			self.formato_exp('float', 11, self.total_1er_venc),
			self.formato_exp('float', 11, self.total_2do_venc),
		))
		return ''.join(data_trailer)


	def formato_exp(self, tipo, long, val, format_date=False):
		''' Conversor al formato exp. Retorna un str en el formato solicitado. '''
		if not val:
			valor = 0 if tipo in ['int', 'float', 'date'] else ' '
		else:
			valor = val
		if tipo == 'char':
			output = str(valor).ljust(long)
		else:
			if tipo == 'float' and valor != 0:
				str_dos_decimales = "{:.2f}".format(valor)
				s_punto = re.sub('[.]', '', str_dos_decimales)
				output = s_punto.zfill(long)
			if tipo == 'date' and valor != 0:
				output = str(valor.strftime(format_date)).zfill(long)
			if tipo == 'int' or valor == 0:
				output = str(valor).zfill(long)
		return output[0:long]



	# Funciones generadoras de barcode y cpe. Generan y guardan en base de datos un barcode y cpe por factura.
	def cpe(self, c):
		''' Generador de CPE. Recibe un credito. Retorna un str. '''
		data_cpe = [
			self.formato_exp('int', 4, c.consorcio.exp.first().codigo_exp),
			self.formato_exp('int', 4, c.consorcio.id),
			self.formato_exp('int', 5, c.socio.id),
		]
		dv1 = self.dv(''.join(data_cpe))
		data_cpe.append(self.formato_exp('int', 1, dv1))
		return ''.join(data_cpe)


	def barcode(self, c):
		''' Generador de barcode. Recibe un credito. Retorna un str. '''
		fecha1 = c.expensas_pagas(0)
		fecha2 = c.expensas_pagas(1)
		saldo1 = c.saldo(fecha1)
		saldo2 = c.saldo(fecha2)
		if fecha2:
			dif = abs(fecha2 - fecha1).days
		else:
			dif = 0
		data_barcode = [
			self.formato_exp('int', 4, 2634),
			self.formato_exp('int', 4, c.consorcio.id),
			self.formato_exp('int', 5, c.socio.id),
			self.formato_exp('date', 6, fecha1, '%y%m%d'),
			self.formato_exp('float', 7, saldo1),
			self.formato_exp('int', 2, dif),
			self.formato_exp('float', 7, saldo2),
			self.formato_exp('int', 2, 0),
			self.formato_exp('float', 7, 0),
			self.formato_exp('int', 6, c.consorcio.exp.first().di_exp),
			self.formato_exp('int', 4, c.consorcio.exp.first().codigo_exp),
		]
		dv1 = self.dv(''.join(data_barcode))
		data_barcode.append(self.formato_exp('int', 1, dv1))
		dv2 = self.dv(''.join(data_barcode))
		data_barcode.append(self.formato_exp('int', 1, dv2))

		final = ''.join(data_barcode)

		guardar_barcode = Preference(
			documento=c,
			barcode=final,
			cpe=self.cpe(c)
		)
		guardar_barcode.save()

		return final


	def dv(self, data_barcode):
		''' Generador de digito verificador. Recibe un str. Retorna un int.'''
		barcode = data_barcode[1:]
		verificador_data = [3,5,7,9]
		result = int(data_barcode[0])
		indice = 0
		for i in barcode:
			y = int(i)*verificador_data[indice%4]
			result += y
			indice = indice + 1
		result = result / 2
		result = int(result) % 10
		return result

