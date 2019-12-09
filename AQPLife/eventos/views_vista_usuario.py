from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.detail import DetailView
from reportlab.pdfgen import canvas

import qrcode
import io


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


class EventosInscritoView(View):

	template_name = 'eventos/eventos_inscrito.html'
	context={

	}
	def get(self, request, *args, **kwargs):
		profile 		=Profile.objects.get(user=request.user.id)
		list_inscritos 	=Inscrito.objects.filter(profile=profile.id)
		self.context['list_inscritos']=list_inscritos
		return render(request, self.template_name,self.context)

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
    template_name         ='eventos/inscribirse.html'
    context                ={

    }
    def get(self,request,*args,**kwargs):
        profile = Profile.objects.get(user=request.user.id)
        evento = Evento.objects.get(pk=self.kwargs.get("evento_id"))
        inscrito = Inscrito.objects.get(evento=evento.id, profile=profile.id) or None
        self.context['inscrito'] = inscrito
        self.context['evento'] = evento

        if request.GET.get('descargar_credenciales'):
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = io.BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
            img = qrcode.make(inscrito.codigo_inscripcion)
            img.save("qr.jpg")
            pdf.drawString(250,800, 'CREDENCIALES')
            pdf.drawString(100,740, 'Apellidos: ')
            pdf.drawString(100,700, 'Nombres: ')
            pdf.drawString(100,660, 'Evento: ')
            pdf.drawString(250,740, profile.user.last_name)
            pdf.drawString(250,700, profile.user.first_name)
            pdf.drawString(250,660, evento.nombre)
            pdf.drawImage('qr.jpg', 180, 380, 220, 220,preserveAspectRatio=True)                
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response


        return render(request,self.template_name,self.context)


    def post(self, request, *args, **kwargs):
        evento                         =    Evento.objects.get(pk=self.kwargs.get("evento_id"))
        profile                     =    Profile.objects.get(user=request.user.id)
        self.context['evento']        =    evento
        try:
            transaccion                 =     Transaccion.objects.filter(numero_factura=request.POST.get('codigo')).update(estado_transaccion='aprobado')
            inscrito                     =     Inscrito.objects.filter(evento=evento.id,profile=profile).update(estado_inscripcion=True)
        except:
            print("Transaccion no encontrada")
        inscrito                =    Inscrito.objects.get(evento=evento.id,profile=profile.id)
        self.context['inscrito']    =    inscrito
        print(inscrito)
        return render(request,self.template_name,self.context)