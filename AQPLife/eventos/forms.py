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

class CrearPaqueteForm(forms.ModelForm):
	actividad			= forms.ModelMultipleChoiceField(queryset = Actividad.objects.all())

	
	class Meta:
		model=Paquete
		fields=[
				'evento',
				'nombre',
				'costo',
				'actividad',
				'descripcion'
				
			]
		widgets={
			'evento':forms.TextInput(attrs={'class':'input ', 'style':'display:none' ,'type':'hidden'}),
			
		}
	def __init__(self,*args,**kwargs):
		evento=kwargs.pop('instance_evento',None)
		super(CrearPaqueteForm, self).__init__(*args, **kwargs)
		if evento:
			self.fields['evento'].initial=evento.id
			self.fields['actividad'] = forms.ModelMultipleChoiceField(queryset=Actividad.objects.filter(evento=evento.id))