# Generated by Django 4.0.8 on 2022-11-03 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0003_alter_datosadicionales_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosadicionales',
            name='fecha_registro',
        ),
        migrations.RemoveField(
            model_name='datosadicionales',
            name='fecha_ultimo_ingreso',
        ),
    ]
