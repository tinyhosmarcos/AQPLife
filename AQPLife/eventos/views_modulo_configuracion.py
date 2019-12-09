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
from datetime import timedelta
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import io


def Registrar_Asistencia(codigo_inscripcion, actividad):
    try :
        inscrito = Inscrito.objects.get(codigo_inscripcion=codigo_inscripcion)
        lista_actividades = inscrito.paquete.actividad.all()
        asistencia = False
        if actividad in lista_actividades:
            asistencia = True
            try:
                asistio = Asistencia.objects.get(actividad=actividad, inscrito=inscrito)
            except Asistencia.DoesNotExist:
                asistio = None

            if asistio is not None:
                print('ASISTENCIA YA REGISTRADA')
                return False
            else:
                print('ASISTENCIA NO REGISTRADA')
                Asistencia(tipo_asistencia='actividad', inscrito=inscrito, actividad=actividad).save()
                return True
    except Inscrito.DoesNotExist:
        return False

def Puede_Generar(inscrito):
    evento = inscrito.evento
    try:
        lista_actividades = list(Actividad.objects.filter(evento=evento))
    except Actividad.DoesNotExist:
        lista_actividades = []

    try:
        lista_asistencias = list(Asistencia.objects.filter(actividad__in=lista_actividades, inscrito=inscrito))
    except Asistencia.DoesNotExist:
        lista_asistencias = []
        return False
    
    if len(lista_asistencias) >= 0.7 * len(lista_actividades): # si asistio a mas del 70%
        return True
    return False


def Lista_Asistentes(actividad):
    try:
        asistentes = Asistencia.objects.filter(actividad=actividad)
    except Asistencia.DoesNotExist:
        asistencia = []
    try:
        lista_paquetes = Paquete.objects.filter(actividad=actividad)
        inscritos = Inscrito.objects.filter(paquete__in=lista_paquetes).distinct()
    except Paquete.DoesNotExist:
        inscritos = []

    return asistentes, inscritos

def Obtener_Montos(evento, fecha=None):
    lista_ingresos = []
    lista_egresos = []
    lista_transacciones = []
    if fecha is None:
        try:
            lista_transacciones = Transaccion.objects.filter(evento=evento)
        except Transaccion.DoesNotExist:
            lista_transacciones = []
    else:
        try:
            lista_transacciones = Transaccion.objects.filter(evento=evento, fecha=fecha)
        except Transaccion.DoesNotExist:
            lista_transacciones = []

    for t in lista_transacciones:
        if t.estado_transaccion == 'aprobado':
            if t.tipo_transaccion == 'compra':
                lista_ingresos.append(t)
            if t.tipo_transaccion == 'venta':
                lista_egresos.append(t)
    return lista_ingresos, lista_egresos


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

    def get(self,request,*args,**kwargs):
        _id=self.kwargs.get("evento_id")
        evento = Evento.objects.get(id=_id)
        if request.GET.get('generar_certificados'):
            try:
                inscritos = Inscrito.objects.filter(evento=evento)
            except Inscrito.DoesNotExist:
                inscritos = [] 
            response = HttpResponse(content_type='application/pdf')
            from reportlab.lib.pagesizes import letter, landscape
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
            for i in inscritos:
                if Puede_Generar(i) is True:
                    pdf.drawImage('logo_events.png', 50, 430, 150, 150,preserveAspectRatio=True)                
                    pdf.setFont('Helvetica-Bold', 26)
                    pdf.drawString(250, 500, 'Certificado de Asistencia')
                    pdf.setFont('Helvetica', 12)
                    pdf.drawCentredString(400, 450, 'Por la presente se certifica que')
                    pdf.setFont('Helvetica', 18)
                    msg = i.profile.user.first_name + ' ' + i.profile.user.last_name
                    msg += ' ha participado en el evento '
                    msg += evento.nombre
                    pdf.drawCentredString(420, 280, msg)
                    msg = 'realizado entre los días '
                    msg += evento.fecha_inicio.strftime('%d/%m/%Y')
                    msg += ' a '
                    msg += evento.fecha_fin.strftime('%d/%m/%Y')
                    pdf.drawString(230, 260, msg)
                    pdf.setFont('Helvetica-Bold', 20)
                    pdf.drawString(350, 140, 'Make Events')
                    pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        if request.GET.get("reporte_asistencia"):
            try:
                actividades = Actividad.objects.filter(evento=evento)
            except Inscrito.DoesNotExist:
                actividades = [] 
                
            response = HttpResponse(content_type='application/pdf')         
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer)
            for a in actividades:
                asistentes, inscritos = Lista_Asistentes(a)
                pdf.setFont('Helvetica-Bold', 24)
                pdf.drawCentredString(300, 800, 'Actividad: ' + a.nombre)
                pdf.setFont('Helvetica-Bold', 18)
                pdf.drawString(50, 760, 'Inscritos: ')
                pdf.setFont('Helvetica', 12)
                pdf.setFont('Helvetica-Bold', 18)
                pdf.drawString(350, 760, 'Asistieron: ')
                pdf.setFont('Helvetica', 12)
                offset = 20
                pos_ins = 720
                pos_asi = 720
                for ins in inscritos:
                    pdf.drawString(50, pos_ins, ins.profile.user.first_name + ' ' + ins.profile.user.last_name)
                    pos_ins -= offset
                for asi in asistentes:
                    pdf.drawString(350, pos_asi, asi.inscrito.profile.user.first_name + ' ' + asi.inscrito.profile.user.last_name)
                    pos_asi -= offset
                pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        if request.GET.get("reporte_paquete"):
            try:
                lista_actividades = Actividad.objects.filter(evento=evento)
            except Inscrito.DoesNotExist:
                lista_actividades = []

            lista_paquetes = Paquete.objects.filter(actividad__in=lista_actividades).distinct()
            response = HttpResponse(content_type='application/pdf')         
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer)
            for paquete in lista_paquetes:
                lista_inscritos = Inscrito.objects.filter(paquete=paquete).distinct()
                pdf.setFont('Helvetica-Bold', 24)
                pdf.drawCentredString(300, 800, 'Paquete: ' + paquete.nombre)
                pdf.setFont('Helvetica-Bold', 18)
                pdf.drawString(50, 760, 'Inscritos: ')
                pdf.setFont('Helvetica', 12)
                offset = 20
                pos_ins = 720
                pos_asi = 720
                for ins in lista_inscritos:
                    pdf.drawString(50, pos_ins, ins.profile.user.first_name + ' ' + ins.profile.user.last_name)
                    pos_ins -= offset
                pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        if request.GET.get("caja_dia"):
            response = HttpResponse(content_type='application/pdf')         
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer)
            fecha = evento.fecha_inicio
            while fecha <= evento.fecha_fin:
                total_ingresos = 0
                total_egresos = 0
                pdf.setFont('Helvetica-Bold', 24)
                pdf.drawCentredString(300, 800, 'Día: ' + fecha.strftime('%y - %m - %d'))
                ingresos, egresos = Obtener_Montos(evento, fecha)
                pos = 720
                pdf.setFont('Helvetica-Bold', 16)
                pdf.drawString(50, pos + 20, 'Ingresos')
                pdf.setFont('Helvetica', 12)
                for i in ingresos:
                    pdf.drawString(50, pos, i.motivo + ' : S./' + str(i.cantidad) )
                    total_ingresos += i.cantidad
                    pos -= 20
                pdf.setFont('Helvetica', 12)
                pdf.drawString(50, pos-20, 'Total Ingresos : S./' + str(total_ingresos) )
                pos -= 20
                pdf.setFont('Helvetica-Bold', 16)
                pdf.drawString(50, pos-20 , 'Egresos')
                pos -= 20
                pdf.setFont('Helvetica', 12)
                for i in egresos:
                    pdf.drawString(50, pos, i.motivo + ' : S./' + str(i.cantidad) )
                    total_egresos += i.cantidad
                    pos -= 20
                    pdf.setFont('Helvetica', 12)
                pdf.drawString(50, pos-20, 'Total Engresos : S./' + str(total_egresos) )

                fecha += timedelta(days=1)
                pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
        if request.GET.get("caja_evento"):
            response = HttpResponse(content_type='application/pdf')         
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer)
            pdf.setFont('Helvetica-Bold', 24)
            pdf.drawCentredString(300, 800, 'Evento: ' + evento.nombre)
            total_ingresos = 0
            total_egresos = 0
            pdf.setFont('Helvetica-Bold', 24)
            ingresos, egresos = Obtener_Montos(evento)
            pos = 720
            pdf.setFont('Helvetica-Bold', 16)
            pdf.drawString(50, pos + 20, 'Ingresos')
            pdf.setFont('Helvetica', 12)
            for i in ingresos:
                pdf.drawString(50, pos, i.motivo + ' : S./' + str(i.cantidad) )
                total_ingresos += i.cantidad
                pos -= 20
            pdf.setFont('Helvetica', 12)
            pdf.drawString(50, pos-20, 'Total Ingresos : S./' + str(total_ingresos) )
            pos -= 20
            pdf.setFont('Helvetica-Bold', 16)
            pdf.drawString(50, pos-20 , 'Egresos')
            pos -= 20
            pdf.setFont('Helvetica', 12)
            for i in egresos:
                pdf.drawString(50, pos, i.motivo + ' : S./' + str(i.cantidad) )
                total_egresos += i.cantidad
                pos -= 20
                pdf.setFont('Helvetica', 12)
            pdf.drawString(50, pos-20, 'Total Engresos : S./' + str(total_egresos) )

            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        return super(EventoDetailView, self).get(request, *args, **kwargs)




class ModificarEventoDetailView(DetailView):
    template_name        ='eventos/modificar_evento.html'
    context             ={

    }
    def get_object(self):
        _id             =self.kwargs.get("evento_id")
        return get_object_or_404(Evento,id=_id)
        
    def get(self, request, *args, **kwargs):
        
        evento_tmp         =get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
        form             =ModificarEventoForm(request.POST or None, instance=evento_tmp)
        self.context['form']                =form
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        evento_tmp         =get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
        form             =ModificarEventoForm(request.POST or None, instance=evento_tmp)
        if form.is_valid():
            print("entro post")
            form.save()
            return redirect('eventos:evento',evento_id=self.kwargs.get("evento_id"))
        evento_tmp         =get_object_or_404(Evento,id=self.kwargs.get("evento_id"))
        form             =ModificarEventoForm(request.POST or None, instance=evento_tmp)
        return render(request, self.template_name,self.context)
    
class CrearEventoDetailView(DetailView):
    template_name         ='eventos/crear_evento.html'
    context               ={

    }
    def  get_object(self):
        _id=self.kwargs.get("user_id")
        return get_object_or_404(Profile,user=_id)

    def get(self, request, *args, **kwargs):
        form                                 =CrearEventoForm()
        self.context['form']                =form
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        form              = CrearEventoForm(request.POST)
        if form.is_valid():
            evento         =form.save();
            personal      =Personal.objects.create(profile_id=self.kwargs.get("user_id"),evento_id=evento.id,categoria_personal_id=1)
        return render(request, self.template_name,self.context)

class Gestionar_MaterialDetailView(DetailView):
    template_name        ='eventos/gestionar_material.html'
    context             ={

    }
    def  get_object(self):
        _id=self.kwargs.get("evento_id")
        return get_object_or_404(Evento,id=_id)

class Gestionar_AmbienteDetailView(DetailView):
    template_name        ='eventos/gestionar_ambiente.html'
    context             ={
    }
    
    def get(self, request, *args, **kwargs):
        evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']                =evento
        form                                 =CrearAmbienteForm()
        form.fields['evento'].initial        =evento.id
        self.context['form']                =form
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        form              = CrearAmbienteForm(request.POST)
        evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))    
        self.context['evento']                =evento
        if form.is_valid():
            ambiente         =form.save();
        form                                 =CrearAmbienteForm()
        self.context['form']                =form
        return render(request, self.template_name,self.context)


class Gestionar_ActividadDetailView(DetailView):
    template_name        ='eventos/gestionar_actividad.html'
    context             ={

    }
    def get(self, request, *args, **kwargs):
        evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']                =evento
        form                                 =CrearActividadForm()
        form.fields['evento'].initial        =evento.id
        self.context['form']                =form
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        form              = CrearActividadForm(request.POST)
        evento= Evento.objects.get(pk=self.kwargs.get("evento_id"))    
        self.context['evento']                =evento
        
        print(form.data['ambiente'])
        if form.is_valid():
            
            print("entro")
            form.save()
        form                                 =CrearActividadForm()
        form.fields['evento'].initial        =evento.id
        self.context['form']                =form
        return render(request, self.template_name,self.context)

class Gestionar_PaqueteDetailView(DetailView):
    """docstring for Gestionar_paqueteDetailView"""
    template_name        ='eventos/gestionar_paquete.html'
    context             ={

    }

    def get(self, request, *args, **kwargs):
        evento                         =    Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']        =    evento
        form                         =     CrearPaqueteForm(instance_evento=evento)
        self.context['form']        =    form
        return render(request,self.template_name,self.context)



    def post(self, request, *args, **kwargs):
        print(request.POST)
        form              = CrearPaqueteForm(request.POST)
        if form.is_valid():
            print("entro")
            evento         =form.save();
        else:
            print("vuelva a llenar el formulario")
        evento                         =    Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                         =     CrearPaqueteForm(instance_evento=evento)
        self.context['form']        =    form        
        return render(request, self.template_name,self.context)

class Gestionar_PersonalDetailView(DetailView):
    """docstring for Gestionar Personal"""
    template_name        ='eventos/gestionar_personal.html'
    context             ={

    }
    def get(self, request, *args, **kwargs):
        evento                         =    Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                         =     CrearPersonalForm(instance_evento=evento)
        self.context['evento']        =    evento
        self.context['form']        =    form    
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form             = CrearPersonalForm(request.POST)
        if form.is_valid():
            print("entro")
            evento         =form.save()
        else:
            print("no entro")


class Gestionar_AsistenciaDetailView(DetailView):
    """docstring for ClassName"""
    template_name = 'eventos/gestionar_asistencia.html'
    context = {}
    def get(self, request, *args, **kwargs):
        evento                         =    Evento.objects.get(pk=self.kwargs.get("evento_id"))
        lista_actividades             =     Actividad.objects.filter(evento=evento)
        self.context['evento']        =    evento
        self.context['lista_actividades']     =     lista_actividades
        context_copy = self.context
        if request.GET:
            lista_paquetes             =     Paquete.objects.filter(actividad=request.GET.get('actividad'))
            lista_inscritos            =     Inscrito.objects.filter(paquete__in=lista_paquetes).distinct()
            self.context['lista_inscritos']    = lista_inscritos
            self.context['actividad'] = Actividad.objects.get(pk=request.GET.get('actividad'))
            try:
                lista_asistentes = Asistencia.objects.filter(actividad=self.context['actividad'])
            except Asistencia.DoesNotExist:
                lista_asistentes = []
            self.context['lista_asistentes'] = lista_asistentes

            cap = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_PLAIN

            while True:
                _, frame = cap.read()
                decodedObjects = pyzbar.decode(frame)
                for obj in decodedObjects:
                    cv2.putText(frame, "Codigo: " + str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)
                    asistencia = Registrar_Asistencia(obj.data, self.context['actividad'])
                    if asistencia is False:
                        cv2.putText(frame, "Asistencia ya fue registrada", (100, 100), font, 2, (255, 0, 0), 3)


                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1)
                if key == 27:
                    cap.release()
                    return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form             = CrearPersonalForm(request.POST)
        if form.is_valid():
            print("entro")
            evento         =form.save()
        else:
            print("no entro")

class Gestionar_ExpositorDetailView(DetailView):
    """Controlador para Gestionar Expositor"""
    template_name       ='eventos/gestionar_expositor.html'
    context             ={

    }

    def get(self, request, *args, **kwargs):
        lista_expositor             =   Expositor.objects.all()
        self.context['lista_expositor']=    lista_expositor
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']      =   evento
        form                        =   CrearExpositorForm(instance_evento=evento)
        self.context['form']        =   form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        lista_expositor             =   Expositor.objects.all()
        self.context['lista_expositor']=    lista_expositor
        print(request.POST)
        form            = CrearExpositorForm(request.POST)
        if form.is_valid():
            print("entro")
            evento      =form.save();
        else:
            print("vuelva a llenar el formulario")
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                        =   CrearExpositorForm(instance_evento=evento)
        self.context['form']        =   form        
        return render(request, self.template_name,self.context)

class Gestionar_PersonalDetailView(DetailView):
    """Controlador para Gestionar Personal"""
    template_name       ='eventos/gestionar_personal.html'
    context             ={

    }
    def get(self, request, *args, **kwargs):
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                        =   CrearPersonalForm(instance_evento=evento)
        self.context['evento']      =   evento
        self.context['form']        =   form    
        return render(request, self.template_name,self.context )

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form            = CrearPersonalForm(request.POST)
        if form.is_valid():
            print("entro")
            evento      =form.save()
        else:
            print("no entro")

class Gestionar_PreInscritoDetailView(DetailView):
    """Controlador para Gestionar Paquete"""
    template_name       ='eventos/gestionar_preinscrito.html'
    context             ={

    }

    def get(self, request, *args, **kwargs):
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']      =   evento
        preinscrito                 =   Inscrito.objects.filter(evento=evento.id,estado_inscripcion=False).count()
        self.context['preinscrito'] =   preinscrito
        return render(request,self.template_name,self.context)



    def post(self, request, *args, **kwargs):
        print(request.POST)
        form            = CrearPaqueteForm(request.POST)
        if form.is_valid():
            print("entro")
            evento      =form.save();
        else:
            print("vuelva a llenar el formulario")
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                        =   CrearPaqueteForm(instance_evento=evento)
        self.context['form']        =   form        
        return render(request, self.template_name,self.context)


class Gestionar_InscritoDetailView(DetailView):
    """Controlador para Gestionar Paquete"""
    template_name       ='eventos/gestionar_inscrito.html'
    context             ={

    }

    def get(self, request, *args, **kwargs):
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        self.context['evento']      =   evento
        inscrito                    =   Inscrito.objects.filter(evento=evento.id,estado_inscripcion=True).count()
        self.context['inscrito']    =   inscrito
        return render(request,self.template_name,self.context)



    def post(self, request, *args, **kwargs):
        print(request.POST)
        form            = CrearPaqueteForm(request.POST)
        if form.is_valid():
            print("entro")
            evento      =form.save();
        else:
            print("vuelva a llenar el formulario")
        evento                      =   Evento.objects.get(pk=self.kwargs.get("evento_id"))
        form                        =   CrearPaqueteForm(instance_evento=evento)
        self.context['form']        =   form        
        return render(request, self.template_name,self.context)