from django.contrib import admin

from apps.recibo.models import TipoOperacion, SistemLogs, DatosAdicionales, Difusion

# Register your models here.
admin.site.register(TipoOperacion)
admin.site.register(SistemLogs)

class DatosAdicionalesAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 
        'documento',
        'nombre',
        'apellido',
        'email',
        'telefono'
        )
    search_fields = ['documento','usuario__username']

admin.site.register(DatosAdicionales, DatosAdicionalesAdmin)

admin.site.register(Difusion)