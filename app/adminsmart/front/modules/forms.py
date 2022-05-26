from django import forms
# from django.contrib.auth.models import User
# from django.forms import Textarea, TextInput, NullBooleanSelect, Select, HiddenInput
from adminsmart.apps.core.models import (
	Naturaleza,
	Taxon,
	Cuenta,
	Titulo,
	Metodo,
)

from adminsmart.api.core.serializers import (
	CuentaModelSerializer,
	TituloModelSerializer,
	MetodoModelSerializer
)
# from django.db.models import Q



class FormControl:

	def __init__(self, context={}, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.serializer_context = context
		for field in iter(self.fields):
			clase = 'form-control'
			if "fecha" in field:
				clase += ' datepicker-autoclose'
			self.fields[field].widget.attrs.update({'class': clase})
			if field == "titulo":
				self.fields[field].widget.attrs.update({'readonly': True})

	def is_valid(self):
		self.cleaned_data = self.data
		serializer = self.SERIALIZER(self.instance, data=self.cleaned_data , context=self.serializer_context)
		is_valid = serializer.is_valid()
		self.validated_data = serializer.validated_data
		self._errors = serializer.errors
		return is_valid

	def save(self):
		if self.instance and self.instance.pk:
			serializer = self.SERIALIZER(self.instance, data=self.validated_data, context=self.serializer_context)
			return serializer.update(self.instance, self.validated_data)
		serializer = self.SERIALIZER(data=self.validated_data, context=self.serializer_context)
		return serializer.create(self.validated_data)


class CuentaForm(FormControl, forms.ModelForm):

	SERIALIZER = CuentaModelSerializer

	class Meta:
		model = Cuenta
		fields = ['nombre', 'numero', 'taxon', 'perfil', 'domicilio', 'titulo']
		labels = {
			'taxon': 'Tipo',
			'titulo': 'Título contable',
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if kwargs['context']['naturaleza'] in ['gasto', 'caja', 'ingreso']:
			self.fields.pop('numero')
			self.fields.pop('perfil')
			self.fields.pop('domicilio')
			self.fields['taxon'].queryset = Taxon.objects.filter(naturaleza__nombre=kwargs['context']['naturaleza'])
			if kwargs['context']['naturaleza'] in ['ingreso']:
				for t in ['interes', 'descuento']:
					self.fields[t] = forms.ModelChoiceField(
						queryset=Metodo.objects.filter(comunidad=kwargs['context']['comunidad'],naturaleza=t),
					)
					self.fields[t].widget.attrs.update({"class": "form-control"})
					if self.instance:
						t_initial = self.instance.metodos.filter(naturaleza=t).first()
						self.fields[t].initial = t_initial.id if t_initial else None
						self.fields[t].required = False
		elif kwargs['context']['naturaleza'] in ['cliente', 'dominio', 'proveedor', 'grupo']:
			self.fields.pop('nombre')
			self.fields.pop('numero')
			self.fields.pop('taxon')
			self.fields.pop('perfil')
			self.fields.pop('domicilio')

		self.fields['titulo'].queryset = Titulo.objects.filter(comunidad=kwargs['context']['comunidad']).order_by("numero")


class TituloForm(FormControl, forms.ModelForm):

	SERIALIZER = TituloModelSerializer

	class Meta:
		model = Titulo
		fields = ['nombre', 'numero','supertitulo','predeterminado']
		labels = {
			'supertitulo': 'Rubro al que pertenece',
			'predeterminado': 'Predeterminado para módulo',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['supertitulo'].queryset = Titulo.objects.filter(comunidad=kwargs['context']['comunidad'], supertitulo__isnull=True).order_by('numero')
		self.fields['predeterminado'].queryset = Naturaleza.objects.all()


class MetodoForm(FormControl, forms.ModelForm):

	SERIALIZER = MetodoModelSerializer

	class Meta:
		model = Metodo
		fields = ['nombre','tipo','plazo','monto','reconocimiento','base_calculo']   

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if kwargs['context']['naturaleza'] in ['descuento']:
			self.fields.pop('reconocimiento')
			self.fields.pop('base_calculo')
