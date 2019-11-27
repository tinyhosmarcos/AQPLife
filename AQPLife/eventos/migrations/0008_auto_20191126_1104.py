# Generated by Django 2.2.7 on 2019-11-26 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_auto_20191126_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(11, 4, 1, 17686)),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='codigo_inscripcion',
            field=models.IntegerField(default=3953638),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='estado_inscripcion',
            field=models.BooleanField(choices=[(False, 'Pre-Inscrito'), (True, 'Inscrito')], default=False),
        ),
    ]
