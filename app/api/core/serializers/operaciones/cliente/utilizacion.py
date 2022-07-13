from datetime import date
from itertools import chain

from api.core.serializers.operaciones.base import *
from api.core.serializers.estados.saldos import *


class UtilizacionModelSerializer(OperacionModelSerializer):
	'''Operacion de utilizacion de saldo a favor o cheques'''

	origen = serializers.SerializerMethodField()

	class Meta:
		model = Operacion

		fields = (
			'id',
			'detalle',
			'origen'
		)


	def __init__(self, *args, **kwargs):
		initial_saldos = kwargs.pop('initial_saldos')
		instance_method = kwargs.pop('instance_method')
		super().__init__(*args, **kwargs)
		if initial_saldos == "disponibilidades":
			queryset = []
			for c in Cuenta.objects.filter(comunidad=self.context['comunidad'], naturaleza__nombre="caja"):
				queryset = list(chain(queryset, c.estado_saldos()))
		else:
			queryset = self.context['cuenta'].estado_saldos()
		if self.instance:
			queryset = list(chain(queryset, getattr(self.instance, instance_method)()))
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=queryset, 
				allow_null=False
			)
		self.fields['vinculo'].display_value = self.display_vinculo

	def get_origen(self, obj):
		if 'retrieve' in self.context.keys():
			context = {
				'end_date': date.today(),
				'condonacion': False
			}
			return EstadoSaldosSerializer(queryset=[obj.origen()], context=context).data[0]
		return ""