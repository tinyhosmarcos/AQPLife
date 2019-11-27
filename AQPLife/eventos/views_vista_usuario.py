from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.detail import DetailView


class IndexView(View):

	template_name = 'eventos/index.html'
	context={

	}
	def get(self, request, *args, **kwargs):
		list_eventos  = Evento.objects.all().order_by('-id')[:5]
		self.context['eventos_list']=list_eventos
		return render(request, self.template_name,self.context )

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name,self.context)


class Ver_EventoDetailView(DetailView):
	template_name		='eventos/ver_evento.html'
	context 			={

	}
	def get(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		return render(request,self.template_name,self.context)



	def post(self, request, *args, **kwargs):
		pass

class Pre_InscribirseDetailView(DetailView):
	template_name 		='eventos/pre_inscribirse.html'
	context				={

	}
	def get(self,request,*args,**kwargs):

		profile=Profile.objects.get(user=request.user.id)
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		try:
			inscrito				=	Inscrito.objects.get(evento=evento.id,profile=profile.id)
		except:
			inscrito 				= 	None
		
		form 						= 	PreInscribirseForm(instance_evento=evento,instace_profile=profile)
		self.context['form']		=	form
		self.context['evento']		=	evento
		self.context['inscrito']	=	inscrito
		return render(request,self.template_name,self.context)

	def post(self, request, *args, **kwargs):
		profile 					=	Profile.objects.get(user=request.user.id)
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		form 			= PreInscribirseForm(request.POST)
		if form.is_valid():
			paquete=Paquete.objects.get(pk=request.POST.get('paquete'))
			print("esto",((paquete.costo)%1000000))
			transaccion	= Transaccion.objects.create(evento=evento,
													numero_factura=int(request.POST.get('codigo_inscripcion'))%1000000,
													motivo='Pre_inscripcion',
													cantidad=paquete.costo,
													tipo_transaccion='compra',
													estado_transaccion='proceso'
													)
			form_evento 		=form.save()
			

		inscrito				=	Inscrito.objects.get(evento=evento.id,profile=profile.id)
		form 						= 	PreInscribirseForm(instance_evento=evento,instace_profile=profile)
		self.context['form']		=	form
		self.context['inscrito']	=	inscrito
		return render(request,self.template_name,self.context)

class InscribirseDetailView(DetailView):
	template_name 		='eventos/inscribirse.html'
	context				={

	}
	def get(self,request,*args,**kwargs):
		profile 					=	Profile.objects.get(user=request.user.id)
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		try:
			inscrito					=	Inscrito.objects.get(evento=evento.id,profile=profile.id)
			self.context['inscrito']	=	inscrito
		except:
			print("aun no estas preinscrito")
		self.context['evento']		=	evento
		return render(request,self.template_name,self.context)


	def post(self, request, *args, **kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		profile 					=	Profile.objects.get(user=request.user.id)
		self.context['evento']		=	evento
		try:
			transaccion 				= 	Transaccion.objects.filter(numero_factura=request.POST.get('codigo')).update(estado_transaccion='aprobado')
			inscrito 					= 	Inscrito.objects.filter(evento=evento.id,profile=profile).update(estado_inscripcion=True)
		except:
			print("Transaccion no encontrada")
		inscrito				=	Inscrito.objects.get(evento=evento.id,profile=profile.id)
		self.context['inscrito']	=	inscrito
		print(inscrito)
		return render(request,self.template_name,self.context)