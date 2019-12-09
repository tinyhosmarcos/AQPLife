from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.detail import DetailView

#Cada controlador esta asociado con su interfaz a travez de la
#variable template_name
#las interfaces se encuentran en la carpeta templates/eventos con formato .html
class Gestionar_EventoDetailView(DetailView):
	"""Controlador para Gestionar Evento"""
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
	"""Controlador para Modificar Evento"""
	template_name		='eventos/modificar_evento.html'
	context 			={

	}
	def get_object(self):
		_id 			=self.kwargs.get("evento_id")
		return get_object_or_404(Evento,id=_id)
		
	def get(self, request, *args, **kwargs):
		
		evento_tmp 		=get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
		form 			=ModificarEventoForm(request.POST or None, instance=evento_tmp)
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		evento_tmp 		=get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
		form 			=ModificarEventoForm(request.POST or None, instance=evento_tmp)
		if form.is_valid():
			print("entro post")
			form.save()
			return redirect('eventos:evento',evento_id=self.kwargs.get("evento_id"))
		evento_tmp 		=get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
		form 			=ModificarEventoForm(request.POST or None, instance=evento_tmp)
		return render(request, self.template_name,self.context)
	
class CrearEventoDetailView(DetailView):
	"""Controlador para Crear Evento"""
	template_name 		='eventos/crear_evento.html'
	context   			={

	}
	def  get_object(self):
		_id=self.kwargs.get("user_id")
		return get_object_or_404(Profile,user=_id)

	def get(self, request, *args, **kwargs):
		form 								=CrearEventoForm()
		profile 							=Profile.objects.get(user=kwargs.get("user_id"))
		personal_list 						=Personal.objects.filter(profile=profile,categoria_personal=1)
		self.context['personal_list'] 		= personal_list
		self.context['form']				=form
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		form  			= CrearEventoForm(request.POST)
		if form.is_valid():
			evento 		=form.save();
			personal  	=Personal.objects.create(profile_id=self.kwargs.get("user_id"),evento_id=evento.id,categoria_personal_id=1)
		if 'adaptar' in request.POST:
			adaptar  	=Evento.objects.get(pk=request.POST.get('evento_adaptar'))
			evento_create 		=Evento.objects.create(nombre=request.POST.get('nombre'),tipo_evento=adaptar.tipo_evento,
										fecha_inicio=request.POST.get('fecha_inicio'),
										fecha_fin=request.POST.get('fecha_fin'))
			lista_ambientes=Ambiente.objects.filter(evento=adaptar.id)
			print(evento_create.id)
			_id=evento_create.id
			for ambiente in lista_ambientes:
				print(ambiente.nombre)
				adaptar_ambiente=Ambiente.objects.create(nombre=ambiente.nombre+"_"+str(_id),
														evento=evento_create,
														ubicacion=ambiente.ubicacion,
														capacidad=ambiente.capacidad)
			

		return render(request, self.template_name,self.context)

class Gestionar_MaterialDetailView(DetailView):
	template_name		='eventos/gestionar_material.html'
	context 			={

	}
	def  get_object(self):
		_id=self.kwargs.get("evento_id")
		return get_object_or_404(Evento,id=_id)

	def get(self, request,*args,**kwargs):
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']				=evento
		if 'submit_actividad' in request.GET:
			material=MaterialActividad.objects.filter(actividad=request.GET.get('ver_actividad'))
			self.context['material'] 		=material
		if 'submit_ambiente' in request.GET:
			material=MaterialAmbiente.objects.filter(ambiente=request.GET.get('ver_ambiente'))
			self.context['material'] 		=material



		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']				=evento
		if 'send_material_actividad' in request.POST:
			actividad=Actividad.objects.get(pk=request.POST.get('actividad'))
			material_actividad=MaterialActividad.objects.create(
					actividad=actividad,
					nombre=request.POST.get('nombre'),
					cantidad=request.POST.get('cantidad'),
					stock=request.POST.get('stock')
				)
		if 'send_material_ambiente' in request.POST:
			ambiente=Ambiente.objects.get(pk=request.POST.get('ambiente'))
			material_ambiente=MaterialAmbiente.objects.create(
				ambiente=ambiente,
				nombre=request.POST.get('nombre'),
				cantidad=request.POST.get('cantidad'),
				stock=request.POST.get('stock')
				)

		return render(request, self.template_name,self.context )	
class Gestionar_AmbienteDetailView(DetailView):
	"""Controlador para Gestionar Ambiente"""
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
	"""Controlador para Gestionar Actividad"""
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
		
		print(form.data['ambiente'])
		if form.is_valid():
			
			print("entro")
			form.save()
		form 								=CrearActividadForm()
		form.fields['evento'].initial		=evento.id
		self.context['form']				=form
		return render(request, self.template_name,self.context)

class Gestionar_PaqueteDetailView(DetailView):
	"""Controlador para Gestionar Paquete"""
	template_name		='eventos/gestionar_paquete.html'
	context 			={

	}

	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		form 						= 	CrearPaqueteForm(instance_evento=evento)
		self.context['form']		=	form
		return render(request,self.template_name,self.context)



	def post(self, request, *args, **kwargs):
		print(request.POST)
		form  			= CrearPaqueteForm(request.POST)
		if form.is_valid():
			print("entro")
			evento 		=form.save();
		else:
			print("vuelva a llenar el formulario")
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 						= 	CrearPaqueteForm(instance_evento=evento)
		self.context['form']		=	form		
		return render(request, self.template_name,self.context)

class Gestionar_ExpositorDetailView(DetailView):
	"""Controlador para Gestionar Expositor"""
	template_name		='eventos/gestionar_expositor.html'
	context 			={

	}

	def get(self, request, *args, **kwargs):
		lista_expositor				=	Expositor.objects.all()
		self.context['lista_expositor']=	lista_expositor
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		form 						= 	CrearExpositorForm(instance_evento=evento)
		self.context['form']		=	form
		return render(request,self.template_name,self.context)

	def post(self, request, *args, **kwargs):
		lista_expositor				=	Expositor.objects.all()
		self.context['lista_expositor']=	lista_expositor
		print(request.POST)
		form  			= CrearExpositorForm(request.POST)
		if form.is_valid():
			print("entro")
			evento 		=form.save();
		else:
			print("vuelva a llenar el formulario")
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 						= 	CrearExpositorForm(instance_evento=evento)
		self.context['form']		=	form		
		return render(request, self.template_name,self.context)

class Gestionar_PersonalDetailView(DetailView):
	"""Controlador para Gestionar Personal"""
	template_name		='eventos/gestionar_personal.html'
	context 			={

	}
	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 						= 	CrearPersonalForm(instance_evento=evento)
		self.context['evento']		=	evento
		self.context['form']		=	form	
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		print(request.POST)
		form 			= CrearPersonalForm(request.POST)
		if form.is_valid():
			print("entro")
			evento 		=form.save()
		else:
			print("no entro")


class Gestionar_AsistenciaDetailView(DetailView):
	"""Controlador para Gestionar asistencia"""
	template_name 		='eventos/gestionar_asistencia.html'
	context 			={

	}
	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		lista_actividades 			= 	Actividad.objects.filter(evento=evento)
		self.context['evento']		=	evento
		self.context['lista_actividades'] 	= 	lista_actividades
		if (request.GET):
			lista_paquetes 			= 	Paquete.objects.filter(actividad=request.GET.get('actividad'))
			lista_inscritos			= 	Inscrito.objects.filter(paquete__in=lista_paquetes).distinct()
			self.context['lista_inscritos']	=lista_inscritos
			
			self.context['actividad']		=Actividad.objects.get(pk=request.GET.get('actividad'))
			##print(request.GET.get('actividad'))
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		lista_actividades 			= 	Actividad.objects.filter(evento=evento)
		self.context['evento']		=	evento
		#self.context['actividad']	=	Actividad.objects.get(pk=request.GET.get('actividad'))
		print(self.context['lista_inscritos'])
		print(self.context['actividad'])
		for inscrito in self.context['lista_inscritos']:
			if request.POST.get(str(inscrito.id)):
				print(inscrito)
				asistencia= Asistencia.objects.create(tipo_asistencia='actividad',
													inscrito=inscrito,
													actividad=self.context['actividad'],
													fecha=self.context['actividad'].fecha,
													hora=self.context['actividad'].hora_inicio)
		#print(request.GET)
		#print(request.POST)
		return render(request, self.template_name,self.context )


class Gestionar_PreInscritoDetailView(DetailView):
	"""Controlador para Gestionar Paquete"""
	template_name		='eventos/gestionar_preinscrito.html'
	context 			={

	}

	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		preinscrito 				=	Inscrito.objects.filter(evento=evento.id,estado_inscripcion=False).count()
		self.context['preinscrito'] =   preinscrito
		return render(request,self.template_name,self.context)



	def post(self, request, *args, **kwargs):
		print(request.POST)
		form  			= CrearPaqueteForm(request.POST)
		if form.is_valid():
			print("entro")
			evento 		=form.save();
		else:
			print("vuelva a llenar el formulario")
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 						= 	CrearPaqueteForm(instance_evento=evento)
		self.context['form']		=	form		
		return render(request, self.template_name,self.context)


class Gestionar_InscritoDetailView(DetailView):
	"""Controlador para Gestionar Paquete"""
	template_name		='eventos/gestionar_inscrito.html'
	context 			={

	}

	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		inscrito 				    =	Inscrito.objects.filter(evento=evento.id,estado_inscripcion=True).count()
		self.context['inscrito']    =   inscrito
		return render(request,self.template_name,self.context)



	def post(self, request, *args, **kwargs):
		print(request.POST)
		form  			= CrearPaqueteForm(request.POST)
		if form.is_valid():
			print("entro")
			evento 		=form.save();
		else:
			print("vuelva a llenar el formulario")
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 						= 	CrearPaqueteForm(instance_evento=evento)
		self.context['form']		=	form		
		return render(request, self.template_name,self.context)		