# Generated by Django 2.2.7 on 2019-11-28 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0010_auto_20191128_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(13, 17, 7, 314824)),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='codigo_inscripcion',
            field=models.IntegerField(default=1010419),
        ),
    ]
