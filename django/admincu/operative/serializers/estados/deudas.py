from .base import *


class EstadoDeudasModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Deuda
	"""

	saldo = serializers.SerializerMethodField()

	class Meta:
		model = Operacion

		fields = (
			'id',
			'interes',
			'pago_capital',
			'saldo'
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.context['cuenta']:
			if self.context['cuenta'].naturaleza.nombre == "cliente":
				self.fields['concepto'] = serializers.CharField(read_only=True, max_length=150)

	def get_saldo(self, obj):

		return obj.saldo(fecha=self.context['fecha'], condonacion=self.context['condonacion'])	