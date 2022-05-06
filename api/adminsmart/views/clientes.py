from .base import AdminFrontView

class ClientesView(AdminFrontView):

	""" Vista de clientes """

	# model = Liquidacion
	# filterset_class = LiquidacionFilter
	MODULE_NAME = "Clientes"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Saldo total de creditos pendientesdo total de creditos pendientes
		# saldo = Credito.objects.filter(consorcio=consorcio(self.request), fin__isnull=True, liquidacion__estado="confirmado").aggregate(saldo=Sum('capital'))['saldo']
		return context
