from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoOperacion(models.Model):
    titulo = models.CharField(max_length = 30)

    class Meta:
        db_table = 'tipo_operacion'
        verbose_name = 'Tipo de operacion'
        verbose_name_plural = 'Tipos de operaciones'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.titulo)

class SistemLogs(models.Model):
    log_usuario = models.CharField(max_length=40,blank=True, null=True)
    log_nombre = models.CharField(max_length=40,blank=True, null=True)
    log_apellido = models.CharField(max_length=40,blank=True, null=True)
    log_documento = models.IntegerField(blank=True, null=True)
    log_tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.CASCADE)
    log_operacion_detalle = models.CharField(max_length=100)
    log_fecha_operacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sistem_logs'
        verbose_name = 'Log de sistema'
        verbose_name_plural = 'Logs de sistema'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.log_operacion_detalle)

class DatosAdicionales(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    documento = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    telefono = models.PositiveBigIntegerField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'datos_adicionales'
        verbose_name = 'Datos adicionales'
        verbose_name_plural = 'Datos adicionales'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.usuario)

class Difusion(models.Model):
    descripcion = models.CharField(max_length=50, blank=False, null=False)
    imagen = models.ImageField(upload_to='difusion/')

    class Meta:
        db_table = 'difusiones'
        verbose_name = 'Difusion'
        verbose_name_plural = 'Difusiones'
        ordering = ['id']

    def __str__(self):
        return self.descripcion