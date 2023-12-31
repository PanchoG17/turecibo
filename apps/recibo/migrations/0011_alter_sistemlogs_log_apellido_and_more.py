# Generated by Django 4.0.8 on 2022-11-24 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0010_difusion_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemlogs',
            name='log_apellido',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sistemlogs',
            name='log_documento',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sistemlogs',
            name='log_nombre',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sistemlogs',
            name='log_usuario',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
