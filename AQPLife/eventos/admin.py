from django.contrib import admin
from django.db import models
from django import forms
from .models import *

admin.site.register(Evento)
admin.site.register(Profile)
admin.site.register(Ambiente)
admin.site.register(Actividad)
admin.site.register(Paquete)

admin.site.register(Personal)
admin.site.register(MaterialAmbiente)
admin.site.register(MaterialActividad)
admin.site.register(Inscrito)
admin.site.register(CategoriaPersonal)
admin.site.register(Transaccion)
admin.site.register(Expositor)

admin.site.register(PaqueteActividad)
admin.site.register(Asistencia)
