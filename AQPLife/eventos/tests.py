from django.test import TestCase
from .models import Evento, Ambiente, Actividad
from datetime import datetime, date, time


class EventoTestCase(TestCase):
    """Probar que se crean correctamente Eventos."""

    def setUp(self):
        Evento.objects.create(
            nombre="evento1",
            tipo_evento="congreso",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )
        Evento.objects.create(
            nombre="evento2",
            tipo_evento="taller",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )
        Evento.objects.create(  # Esto debería dar error (nombre tiene como mas de 30 caracteres)
            nombre="eventoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo3",
            tipo_evento="taller",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )

        Evento.objects.create(  # Esto debería dar error (Ya existe un Evento con este nombre)
            nombre="evento4",
            tipo_evento="taller",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )

    def test_eventos_created(self):
        evento1 = Evento.objects.get(nombre="evento1")
        evento2 = Evento.objects.get(nombre="evento2")
        self.assertEqual(evento1.nombre, "evento1")
        self.assertEqual(evento2.nombre, "evento2")


class AmbienteTestCase(TestCase):
    """Probar que se crean correctamente Ambientes."""

    def setUp(self):
        Evento.objects.create(
            nombre="evento1",
            tipo_evento="congreso",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )
        event = Evento.objects.get(nombre="evento1")
        Ambiente.objects.create(
            evento=event,
            nombre="Ambiente1",
            ubicacion="av lima 520",
            capacidad=20
        )
        Ambiente.objects.create(  # Esto debería dar error (capacidad negativa)
            evento=event,
            nombre="Ambiente2",
            ubicacion="av ejercito 300",
            capacidad=-20
        )
        Ambiente.objects.create(
            evento=event,
            nombre="Ambiente3",
            ubicacion="urb los guindos a20",
            capacidad=20
        )

        Ambiente.objects.create(  # Esto debería dar error (Ya existe un Ambiente con este nombre)
            evento=event,
            nombre="Ambiente5",
            ubicacion="av lima 520",
            capacidad=20
        )

        Ambiente.objects.create(  # Esto debería dar error (Capacidad muy grande. no realista)
            evento=event,
            nombre="Ambiente4",
            ubicacion="av lima 520",
            capacidad=1000000000000000
        )

    def test_ambientes_created(self):
        Ambiente2 = Ambiente.objects.get(nombre="Ambiente2")
        Ambiente4 = Ambiente.objects.get(nombre="Ambiente4")
        assert Ambiente2.capacidad > 0, "capacidad debe ser mayor a 0"
        assert Ambiente4.capacidad < 1000, "capacidad debe ser menor a 1000"


class ActividadTestCase(TestCase):
    """Probar que se crean correctamente Actividades."""

    def setUp(self):
        event = Evento.objects.create(
            nombre="evento1",
            tipo_evento="congreso",
            fecha_inicio=date.today(), fecha_fin=date.today()
        )
        # event = Evento.objects.get(nombre="evento1")
        ambient = Ambiente.objects.create(
            evento=event,
            nombre="Ambiente1",
            ubicacion="av lima 520",
            capacidad=20
        )

        Actividad.objects.create(
            evento=event,
            ambiente=ambient,
            nombre="Actividad1",
            fecha=date.today(),
            hora_inicio=time(),
            hora_fin=time(22, 8, 24, 78915),
        )

        Actividad.objects.create(  # Esto debería dar error (hora de inicio no puede ser mayor a hora de fin)
            evento=event,
            ambiente=ambient,
            nombre="Actividad2",
            fecha=date.today(),
            hora_inicio=time(15, 8, 24, 78915),
            hora_fin=time(12, 8, 24, 78915),
        )

        Actividad.objects.create(  # Esto debería dar error (hora de inicio no puede ser igual a hora de fin)
            evento=event,
            ambiente=ambient,
            nombre="Actividad3",
            fecha=date.today(),
            hora_inicio=time(),
            hora_fin=time(),
        )

    def test_actividades_created(self):
        Actividad2 = Actividad.objects.get(nombre="Actividad2")
        Actividad3 = Actividad.objects.get(nombre="Actividad3")
        assert Actividad2.hora_inicio < Actividad2.hora_fin, "Hora de inicio debe ser menor a hora de fin"
        assert Actividad3.hora_inicio < Actividad3.hora_fin, "Hora de inicio debe ser menor a hora de fin"


# Create your tests here.
