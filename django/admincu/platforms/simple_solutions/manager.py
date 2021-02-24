from datetime import date
import ftplib
import paramiko
import json

from .models import *
from admincu.operative.models import Documento
from admincu.platforms.expensas_pagas.models import Preference
from admincu.files.models import Archivo

class Conexion():
	"""
		Exportador/Importador ExP class, generador de barcode numerico.
	"""

	clientes = AccountSS.objects.all()
	hoy = date.today()
	hostname = "s-ddd967132e9f42198.server.transfer.us-east-1.amazonaws.com"
	usuario = "admincu"
	# key_path = settings.MEDIA_ROOT + "/admincu_ss"
	opciones = [
		{
			'modelo': 'Documento',
			'carpeta': 'facturas',
			'titulo': 'FACTURA',
			'kwargs': {
				'receipt__receipt_type__code__in': ['11', '51'] 
			}
		},
		{
			'modelo': 'Documento',
			'carpeta': 'recibos',
			'titulo': 'RECIBO',
			'kwargs': {
				'receipt__receipt_type__code__in': ['54'] 
			}
		},		
		{
			'modelo': 'Preference',
			'carpeta': 'cupones',
			'titulo': 'CUPON',
			'kwargs': {}
		}
	]

	# Funciones de exportacion
	def export(self):
		''' Inicializa la clase para crear un acrchivo txt por cliente de Exp.'''

		for cliente in self.clientes:
			for opcion in self.opciones:
				ultimo_enviado = Sent.objects.filter(comunidad=cliente.comunidad, modelo=opcion['modelo'], filtros=json.dumps(opcion['kwargs'])).order_by("-id_modelo").first()
				if ultimo_enviado:
					kwargs = opcion['kwargs']
					kwargs.update({
						'id__gt': ultimo_enviado.id_modelo,
						'comunidad': cliente.comunidad
					})
					documentos = eval(opcion['modelo']).objects.filter(**kwargs)
					if documentos:
						a_enviar, envios = self.procesar(cliente.nombre, documentos, opcion, cliente.comunidad)
						self.upload(cliente.nombre, a_enviar, opcion['carpeta'], envios, cliente.comunidad)
						
					

	def procesar(self, nombre_cliente, documentos, opcion, comunidad):
		documentos_procesados = []
		envios = []
		for d in documentos:
			if opcion['titulo'] == "CUPON":
				destinatario_id = d.documento.destinatario.id
			else:
				destinatario_id = d.documento.id
			documento = {
				'nombre': "{}_{}_{}_{}.pdf".format(nombre_cliente, destinatario_id, opcion['titulo'], d.id),
				'path': d.pdf.path 
			}
			documentos_procesados.append(documento)

			envios.append(Sent(
				comunidad=comunidad,
				modelo=opcion['modelo'],
				id_modelo=d.id,
				fecha_envio=self.hoy,
				filtros=json.dumps(opcion['kwargs'])
			))

		return documentos_procesados, envios

	def upload(self, carpeta_cliente, documentos_procesados, carpeta_documento, envios, comunidad):	
		''' Sube el archivo al servidor de SS. '''
		try:
			ssh_connect = paramiko.SSHClient()
			ssh_connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			key = paramiko.RSAKey.from_private_key_file(Archivo.objects.get(comunidad=comunidad, nombre="Clave SS").ubicacion.path)
			ssh_connect.connect(hostname=self.hostname, username=self.usuario, pkey=key)
			sftp = ssh_connect.open_sftp()
			for d in documentos_procesados:
				remotepath = "/{}/{}/{}".format(carpeta_cliente, carpeta_documento, d['nombre'])
				respuesta = sftp.put(d['path'], remotepath=remotepath)
			
			ssh_connect.close()
			self.save(envios)
		except:
			print('Error al subir archivo')					

	def save(self, envios):
		Sent.objects.bulk_create(envios)