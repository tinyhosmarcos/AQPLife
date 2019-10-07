from django import forms
from .models import *

class CrearEventoForm(forms.ModelForm):
	class Meta:
		model=Evento
		fields=[
			'nombre',
			'tipo_evento',
			'fecha_inicio',
			'fecha_fin'
		]
		widgets={
			'nombre':forms.TextInput(attrs={'class':'input'}),
			'tipo_evento':forms.TextInput(attrs={'class':'input'}),
			'fecha_inicio':forms.TextInput(attrs={'class':'input'}),
			'fecha_fin':forms.TextInput(attrs={'class':'input'})
		}


class ModificarEventoForm(forms.ModelForm):
	class Meta:
		model=Evento
		fields=[
			'nombre',
			'tipo_evento',
			'fecha_inicio',
			'fecha_fin'
		]
		widgets={
			'nombre':forms.TextInput(attrs={'class':'input'}),
			'tipo_evento':forms.TextInput(attrs={'class':'input'}),
			'fecha_inicio':forms.TextInput(attrs={'class':'input'}),
			'fecha_fin':forms.TextInput(attrs={'class':'input'})
		}