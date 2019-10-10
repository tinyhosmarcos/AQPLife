from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView

class IndexView(View):
	eventos_list  = Evento.objects.all()
	template_name = 'eventos/index.html'
	context={
		'eventos_list':eventos_list,

	}
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name,self.context)


class Gestionar_EventoDetailView(DetailView):
	template_name='eventos/gestionar_evento.html'
	def get_context_data(self, **kwargs):
		context = super(Gestionar_EventoDetailView, self).get_context_data(**kwargs)
		context['personals'] = Personal.objects.filter(profile=self.object)
		return context


	def get_object(self):
		_id=self.kwargs.get("user_id")
		return get_object_or_404(Profile,user=_id)


class EventoDetailView(DetailView):
	template_name='eventos/evento.html'
	def  get_object(self):
		_id=self.kwargs.get("evento_id")
		return get_object_or_404(Evento,id=_id)


class ModificarEventoDetailView(DetailView):
	template_name		='eventos/modificar_evento.html'
	context 			={

	}
	def get_object(self):
		_id 			=self.kwargs.get("evento_id")
		return get_object_or_404(Evento,id=_id)
		
	def get(self, request, *args, **kwargs):
		form 			=ModificarEventoForm()
		evento_tmp 		=Evento.objects.get(id=self.kwargs.get("evento_id"))
		form.fields['nombre'].initial		=evento_tmp.nombre
		form.fields['tipo_evento'].initial	=evento_tmp.tipo_evento
		form.fields['fecha_inicio'].initial	=evento_tmp.fecha_inicio
		form.fields['fecha_fin'].initial	=evento_tmp.fecha_fin
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		form = ModificarEventoForm(request.POST)
		if form.is_valid():
			data=request.POST.copy()
			self.object 				=self.get_object()
			self.object.nombre 			=data.get('nombre')
			self.object.tipo_evento 	=data.get('tipo_evento')
			self.object.fecha_inicio 	=data.get('fecha_inicio')
			self.object.fecha_fin 		=data.get('fecha_fin')
			print(data.get('nombre'))
			self.object.save()
			#form=ModificarEventoForm()
			#self.context['form']				=form
		return render(request, self.template_name,self.context)
	
class CrearEventoDetailView(DetailView):
	template_name 		='eventos/crear_evento.html'
	context   			={

	}
	def  get_object(self):
		_id=self.kwargs.get("user_id")
		return get_object_or_404(Profile,user=_id)

	def get(self, request, *args, **kwargs):
		form 								=CrearEventoForm()
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		form  			= CrearEventoForm(request.POST)
		if form.is_valid():
			evento 		=form.save();
			personal  	=Personal.objects.create(profile_id=self.kwargs.get("user_id"),evento_id=evento.id,categoria_personal_id=1)
		return render(request, self.template_name,self.context)

class Gestionar_MaterialDetailView(DetailView):
	template_name		='eventos/gestionar_material.html'
	context 			={

	}
	def  get_object(self):
		_id=self.kwargs.get("evento_id")
		return get_object_or_404(Evento,id=_id)

class Gestionar_AmbienteDetailView(DetailView):
	template_name		='eventos/gestionar_ambiente.html'
	context 			={
	}
	
	def get(self, request, *args, **kwargs):
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']				=evento
		form 								=CrearAmbienteForm()
		form.fields['evento'].initial		=evento.id
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		form  			= CrearAmbienteForm(request.POST)
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))	
		self.context['evento']				=evento
		if form.is_valid():
			ambiente 		=form.save();
		form 								=CrearAmbienteForm()
		self.context['form']				=form
		return render(request, self.template_name,self.context)


class Gestionar_ActividadDetailView(DetailView):
	template_name		='eventos/gestionar_actividad.html'
	context 			={

	}
	def get(self, request, *args, **kwargs):
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']				=evento
		form 								=CrearActividadForm()
		form.fields['evento'].initial		=evento.id
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		form  			= CrearActividadForm(request.POST)
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))	
		self.context['evento']				=evento
		
		if form.is_valid():
			print("entro")
			ambiente 		=form.save();
		form 								=CrearActividadForm()
		form.fields['evento'].initial		=evento.id
		self.context['form']				=form
		return render(request, self.template_name,self.context)
