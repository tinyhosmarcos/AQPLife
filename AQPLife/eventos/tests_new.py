from django.test import TestCase
from .models import Evento, Profile
from datetime import datetime, date, time
from .functions import RegistrarPreinscrito

class TestCase05(TestCase):
    def setUp(self):
        Evento.objects.create(
            nombre="CLEI 2019",
            tipo_evento="Congreso",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )

    def test(self):
        usuario = Profile.objects.get(user="yhostin")
        evento = Evento.objects.get(nombre="CLEI 2019")
        # case 5.1
        RegistrarPreinscrito(usario.id, evento.id)
        # case 5.2
        RegistrarPreinscrito(usario.id, evento.id)

class TestCase06(TestCase):
    def setUp(self):
        Evento.objects.create(
            nombre="CLEI 2019", tipo_evento="Congreso",
            fecha_inicio=date.today(), fecha_fin=date.today())
        Evento.objects.create(
            nombre="CLEI 2018", tipo_evento="Congreso",
            fecha_inicio=datetime.date(2018, 10, 10), fecha_fin=datetime.date(2018, 10, 12))

    def test(self):
        usuario = Profile.objects.get(user="yhostin")
        evento1 = Evento.objects.get(nombre="CLEI 2019")
        evento2 = Evento.objects.get(nombre="CLEI 2019")
        
        RegistrarInscrito(usario.id, evento1.id)  # case 6.1
        RegistrarInscrito(usario.id, evento1.id)  # case 6.2
        RegistrarInscrito(usario.id, evento2.id)  # case 6.3

class TestCase07(TestCase):
    def setUp(self):
        Evento.objects.create(
            nombre="CLEI 2019",tipo_evento="Congreso",
            fecha_inicio=date.today(), fecha_fin=date.today()  )
        Ambiente.objects.create(
            evento=event,nombre="Universidad Católica San Pablo, D04",
            ubicacion="Urb campiña paisajista",capacidad=20 )
    def test(self):
        event = Evento.objects.get(nombre="CLEI 2019")
        ambient = Ambiente.objects.get(nombre="Universidad Católica San Pablo, D04")
        AnadirActividad(  # case 7.1
            evento=event,ambiente=ambient, nombre="Exposicion1",
            fecha=date.today(), hora_inicio=time(8, 0, 0, 0), hora_fin=time(10, 0, 0, 0),
        )

        AnadirActividad( # case 7.2
            evento=event, ambiente=ambient, nombre="Exposicion2",
            fecha=date.today(), hora_inicio=time(9, 0, 0, 0), hora_fin=time(11, 0, 0, 0),
        )

        AnadirActividad( # case 7.3
            evento=event, ambiente=ambient, nombre="Exposicion3",
            fecha=date.today(), hora_inicio=time(10, 0, 0, 0), hora_fin=time(12, 0, 0, 0),
        )

class TestCase13(TestCase):
    def setUp(self):
        Evento.objects.create(
            nombre="CLEI 2019",tipo_evento="Congreso",
            fecha_inicio=date.today(), fecha_fin=date.today() )
        Evento.objects.create(
            nombre="CLEI 2020",tipo_evento="Congreso",
            fecha_inicio=datetime.date(2020, 10, 10), fecha_fin=datetime.date(2020, 10, 14) )
        Ambiente.objects.create(
            evento=event,nombre="Universidad Católica San Pablo, D04",
            ubicacion="Urb campiña paisajista",capacidad=20 )
        AñadirActividad(
            evento=event,ambiente=ambient, nombre="Exposicion1",
            fecha=date.today(), hora_inicio=time(8, 0, 0, 0), hora_fin=time(10, 0, 0, 0) )
        AñadirActividad(
            evento=event, ambiente=ambient, nombre="Exposicion2",
            fecha=date.today(), hora_inicio=time(9, 0, 0, 0), hora_fin=time(11, 0, 0, 0))


    def test(self):
        event1 = Evento.objects.get(nombre="CLEI 2019")
        event2 = Evento.objects.get(nombre="CLEI 2020")
        SeleccionarActividades(event1.id, "Ayudante", ["Exposicion1", "Exposicion2"])  # case 13.1
        SeleccionarActividades(event1.id, "Ayudante", ["Exposicion1", "Exposicion2"])  # case 13.2
        SeleccionarActividades(event2.id, "Ayudante", ["Exposicion1", "Exposicion2"])  # case 13.3
class TestCase14(TestCase):
    def setUp(self):
        Evento.objects.create(
            nombre="CLEI 2019",tipo_evento="Congreso",
            fecha_inicio=date.today(), fecha_fin=date.today() )
        Ambiente.objects.create(
            evento=event,nombre="Universidad Católica San Pablo, D04",
            ubicacion="Urb campiña paisajista",capacidad=20 )
        AñadirActividad(
            evento=event,ambiente=ambient, nombre="Exposicion1",
            fecha=date.today(), hora_inicio=time(8, 0, 0, 0), hora_fin=time(10, 0, 0, 0) )
        AñadirActividad(
            evento=event, ambiente=ambient, nombre="Exposicion2",
            fecha=date.today(), hora_inicio=time(9, 0, 0, 0), hora_fin=time(11, 0, 0, 0))


    def test(self):
        event = Evento.objects.get(nombre="CLEI 2019")
        SeleccionarActividades(event1.id, "Ayudante", ["Exposicion1", "Exposicion2"]) 
        EliminarRol(event.id, "Ayudante")  # case 14.1
        EliminarROl(event.id, "Ayudante")  # case 14.2






