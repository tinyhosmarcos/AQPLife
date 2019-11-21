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
		passdetail

class Pre_InscribirseDetailView(DetailView):
	template_name 		='eventos/pre_inscribirse.html'
	context				={

	}
	def get(self,request,*args,**kwargs):
		evento 						=	Evento.objects.get(pk=self.kwargs.get("evento_id"))
		self.context['evento']		=	evento
		return render(request,self.template_name,self.context)