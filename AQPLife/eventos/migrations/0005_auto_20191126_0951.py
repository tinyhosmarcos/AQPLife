# Generated by Django 2.2.7 on 2019-11-26 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_auto_20191105_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscrito',
            name='codigo_inscripcion',
            field=models.IntegerField(default=1565758),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(9, 51, 38, 889721)),
        ),
    ]
