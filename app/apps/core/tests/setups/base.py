from django.contrib.auth.models import Group

from apps.core.models import *

class OperativeSetUp():

	NATURALEZAS = {
		"cliente": ["socio"], 
		"dominio": ["propietario", "inquilino"], 
		"ingreso": ["prioritario", "no_prioritario", "interes_predeterminado"], 
		"proveedor": [], 
		"caja": ["stockeable", "plataformas", "banco", "efectivo"],
		"gasto": ["comun", "descuento_predeterminado"], 
		"bien_de_cambio": [],
		"bien_de_uso": [],
		"patrimonio": []
	}

	def create_naturalezas(self):
		Naturaleza.objects.bulk_create([Naturaleza(nombre=n) for n in self.NATURALEZAS.keys()])
		self.naturalezas = Naturaleza.objects.all()

	def create_taxones(self):
		for k, v in self.NATURALEZAS.items():
			_nat = self.naturalezas.get(nombre=k)
			for taxon in v:
				Taxon.objects.create(
					naturaleza=_nat,
					nombre=taxon
				)

	# def create_clientes(self):
	# 	_nat = self.naturalezas.get(nombre="cliente")
	# 	Cuenta.objects.bulk_create(*[
	# 		Cuenta(

	# 		)
	# 	])
	# 	self.clientes = Cuenta.objects.filter(naturaleza="cliente")

	def __create__(self):
		self.create_naturalezas()
		self.create_taxones()