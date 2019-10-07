# Generated by Django 2.2 on 2019-09-30 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0008_auto_20190930_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriausuario',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='categoria_usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='eventos.CategoriaUsuario'),
            preserve_default=False,
        ),
    ]