# Generated by Django 2.2.7 on 2019-11-26 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0006_auto_20191126_1010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaccion',
            old_name='factura',
            new_name='numero_factura',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(10, 13, 22, 45579)),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='codigo_inscripcion',
            field=models.IntegerField(default=3619691),
        ),
    ]
