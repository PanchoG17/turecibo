# Generated by Django 4.0.8 on 2022-11-09 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recibo', '0004_remove_datosadicionales_fecha_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosadicionales',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datosadicionales',
            name='telefono',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datosadicionales',
            name='usuario',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
