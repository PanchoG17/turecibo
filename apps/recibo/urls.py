from django.urls import path

from . import views

app_name = 'recibo'

urlpatterns = [
    path('', views.auth_login, name='auth_login'),
    path('logout', views.auth_logout, name='auth_logout'),
    path('home', views.home, name='home'),
    path('listado', views.ver_completo, name='ver_completo'),
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('view_pdf/<str:id_recibo>/<str:periodo>', views.view_pdf, name='view_pdf'),
    path('download_pdf/<str:id_recibo>/<str:periodo>', views.download_pdf, name='download_pdf'),
    path('enviar_mail', views.enviar_mail, name='enviar_mail'),
    path('enviar_mail_banco', views.enviar_mail_banco, name='enviar_mail_banco'),

    path('generate_nomade_pdf', views.generate_nomade_pdf, name='generate_nomade_pdf'),
    path('view_nomade_pdf/<str:title>', views.view_nomade_pdf, name='view_nomade_pdf'),

]