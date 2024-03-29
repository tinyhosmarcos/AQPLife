# Generated by Django 2.2 on 2019-11-02 18:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('hora_inicio', models.TimeField(blank=True)),
                ('hora_fin', models.TimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ambiente',
            fields=[
                ('nombre', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('ubicacion', models.CharField(max_length=30)),
                ('capacidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=20)),
                ('nivel_categoria', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('tipo_evento', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateField(default=datetime.date.today)),
                ('fecha_fin', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='TipoAsistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='identificacion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='tipo_idenficacion',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.CharField(max_length=30)),
                ('motivo', models.CharField(max_length=100)),
                ('cantidad', models.FloatField(default=0)),
                ('tipo_transaccion', models.CharField(max_length=15)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento')),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria_personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.CategoriaPersonal')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('costo', models.FloatField(default=0)),
                ('actividad', models.ManyToManyField(to='eventos.Actividad')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialAmbiente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('ambiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Ambiente')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Actividad')),
            ],
        ),
        migrations.CreateModel(
            name='Inscrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_inscripcion', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento')),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Paquete')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Expositor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=30)),
                ('actividad', models.ManyToManyField(to='eventos.Actividad')),
            ],
        ),
        migrations.AddField(
            model_name='categoriapersonal',
            name='evento',
            field=models.ManyToManyField(to='eventos.Evento'),
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('hora', models.TimeField(default=datetime.time(13, 24, 55, 666502))),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Actividad')),
                ('inscrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Inscrito')),
            ],
        ),
        migrations.AddField(
            model_name='ambiente',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='ambiente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.Ambiente'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Evento'),
        ),
    ]
