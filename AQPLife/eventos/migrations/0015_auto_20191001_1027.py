# Generated by Django 2.2 on 2019-10-01 15:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0014_auto_20190930_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialAmbiente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='material',
        ),
        migrations.RemoveField(
            model_name='ambiente',
            name='material',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(10, 27, 50, 447931)),
        ),
        migrations.DeleteModel(
            name='Material',
        ),
        migrations.AddField(
            model_name='materialambiente',
            name='ambiente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Ambiente'),
        ),
        migrations.AddField(
            model_name='materialactividad',
            name='actividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Actividad'),
        ),
    ]