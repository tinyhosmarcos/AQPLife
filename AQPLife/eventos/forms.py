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
class CrearAmbienteForm(forms.ModelForm):
	class Meta:
		model=Ambiente
		fields=[
			'evento',
			'nombre',
			'ubicacion',
			'capacidad'
		]
		widgets={
			'evento':forms.TextInput(attrs={'class':'input', 'style':'display:none' ,'type':'hidden'	}),
			'nombre':forms.TextInput(attrs={'class':'input'}),
			'ubicacion':forms.TextInput(attrs={'class':'input'}),
			'capacidad':forms.NumberInput(attrs={'class':'input'})
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
class CrearAmbienteForm(forms.ModelForm):
	class Meta:
		model=Ambiente
		fields=[
			'evento',
			'nombre',
			'ubicacion',
			'capacidad'
		]
		widgets={
			'evento':forms.TextInput(attrs={'class':'input', 'style':'display:none' ,'type':'hidden'	}),
			'nombre':forms.TextInput(attrs={'class':'input'}),
			'ubicacion':forms.TextInput(attrs={'class':'input'}),
			'capacidad':forms.NumberInput(attrs={'class':'input'})
		}


class CrearActividadForm(forms.ModelForm):
	class Meta:
		model=Actividad
		fields=[
			'evento',
			'ambiente',
			'nombre',
			'fecha',
			'hora_inicio',
			'hora_fin'
		]
		widgets={
			'evento':forms.TextInput(attrs={'class':'input ', 'style':'display:none' ,'type':'hidden'}),
			'ambiente':forms.TextInput(attrs={'class':'autocomplete input-field','type':'text', 'id':'autocomplete-input'}),
			'nombre':forms.TextInput(attrs={'class':'input'}),
			'fecha':forms.TextInput(attrs={'class':'input'}),
			'hora_inicio':forms.TextInput(attrs={'class':'input'}),
			'hora_fin':forms.TextInput(attrs={'class':'input'})
		}