# Generated by Django 2.2.7 on 2019-12-09 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0011_auto_20191128_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(5, 39, 15, 269844)),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='codigo_inscripcion',
            field=models.IntegerField(default=2620352),
        ),
    ]
