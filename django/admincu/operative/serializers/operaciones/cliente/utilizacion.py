from datetime import date

from admincu.operative.serializers.operaciones.base import *
from admincu.operative.serializers.estados.saldos import *


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
		super().__init__(*args, **kwargs)
		self.fields['vinculo'] = serializers.PrimaryKeyRelatedField(
				queryset=Operacion.objects.filter(
						comunidad=self.context['comunidad'], 
						cuenta__naturaleza__nombre__in=['cliente', 'caja', 'proveedor'],
					), 
				allow_null=False
			)

	def get_origen(self, obj):
		if 'retrieve' in self.context.keys():
			context = {
				'end_date': date.today(),
				'condonacion': False
			}
			return EstadoSaldosSerializer(queryset=[obj.origen()], context=context).data[0]
		return ""