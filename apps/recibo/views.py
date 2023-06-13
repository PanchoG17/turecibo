from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from email.mime.image import MIMEImage
from zeep.helpers import serialize_object
from core.settings import EMAIL_HOST_USER
from pathlib import Path

import os, codecs

## Models
from apps.recibo.models import DatosAdicionales, Difusion

## Forms
from apps.recibo.forms import SignUpForm, LoginForm, EditForm, EditPassForm

# Services
from core.services import *


def handler404(request, exception):
    return render(request, "layouts/404.html", status=404)

def auth_login(request):

    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = LoginForm(request.POST or None)
        msg = None

        if request.method == 'POST':
            if form.is_valid():

                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                if ADWSLogin(username, password):

                    user = authenticate(username=username, password=password)

                    if user is None:
                        try:
                            ### Usuario registrado con cambio de password
                            user = User.objects.get(username=username)
                            user.set_password(password)
                            user.save()
                            user = authenticate(username=username, password=password)
                            login(request, user)
                            addSystemLog(username, 1, ' - Modificación de contraseña')
                            return redirect('/home')

                        except User.DoesNotExist:
                            ### Usuario no registrado
                            register = SignUpForm(request.POST)
                            if register.is_valid():

                                new_user = register.save()

                                dni = ADWSGetDni(username)
                                data = ADWSGetUsuarioYPass(username)
                                datos_adicionales = DatosAdicionales(
                                    usuario = new_user,
                                    nombre = data['Nombre'],
                                    apellido= data['Apellido'],
                                    documento= dni
                                )
                                datos_adicionales.save()

                                new_user = authenticate(username=username, password=password)
                                login(request, new_user)
                                addSystemLog(username, 4)
                                addSystemLog(username, 1, ' - Primer ingreso')
                                return redirect('/home')
                            else:
                                addSystemLog(username, 2, ' - Registro fallido')
                                msg = 'Error al validar los datos.'
                    else:
                        ### Usuario registrado
                        login(request, user)
                        addSystemLog(username, 1)
                        return redirect('/home')
                else:
                    addSystemLog(username, 2, ' - Usuario o clave incorrecta')
                    msg = 'Usuario o clave incorrecta'
            # else:
            #     addSystemLog(username, 2, ' - Error de validación')
            #     msg = 'Error al validar los datos.'

        return render(request, 'home/login.html', {'form':form, 'msg':msg})

def auth_logout(request):
    ## Borrar archivos generados por el usuario
    path = 'tmp/'
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(path):
        if filename.startswith(request.user.username):
            os.remove(os.path.join(path, filename))

    addSystemLog(request.user, 3)
    logout(request)
    return redirect('/')

# Esta función es para los usuarios que expiraron sesión (auto-logout)
@receiver(user_logged_out)
def clean_auto_logout(sender, user, request, **kwargs):
    ## Borrar archivos generados por el usuario
    path = 'tmp/'
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(path):
        if filename.startswith(request.user.username):
            os.remove(os.path.join(path, filename))

@login_required
def home(request):
    recibos = []
    datos = DatosAdicionales.objects.get(usuario_id=request.user.pk)
    editForm = EditForm(instance=datos)
    documento = request.user.datosadicionales.documento

    ## RECIBOS
    recibos_data = RDWSGetRecibosExt(documento)
    if recibos_data is not None:
        for recibo in reversed(recibos_data):
            if len(recibos) < 12:
                if recibo['Firmado'] and '-ANULADO-' not in recibo['Escalafon']:
                #if '-ANULADO-' not in recibo['Escalafon']:
                    recibo = serialize_object(recibo)
                    recibo.move_to_end('Id')
                    recibo.move_to_end('Escalafon', False)
                    recibos.append(recibo)

    ## VALIDACIÓN DOCENTES DDJJ
    docentes_data = MAWSEsDocente(documento)
    docente_activo = False
    control = 0
    if docentes_data is not None:
        for d in docentes_data:
            if d['MaestroEmpresa'] == 'DOCENT' and (d['MaestroEstado'] == '1' or d['MaestroEstado'] == '5'):
                docente_activo = True
                break
    if docente_activo:
        documento = str(documento)
        if len(documento) == 8:
            control = int(documento[0:1]) + int(documento[5:6]) + int(documento[6:7])
        else:
            control = 0 + int(documento[5:6]) + int(documento[6:7])

    ## EDIT REQUEST ##
    if request.method == "POST":
        editForm = EditForm(request.POST, instance=datos)
        if editForm.is_valid():
            editForm.save()
            addSystemLog(request.user, 9)

    ## EDIT PASSWORD ##
    username = request.user.username
    passwordForm = EditPassForm
    msg=''

    if 'oldpassword' in request.POST:
        form = EditPassForm(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data.get("oldpassword")
            password = form.cleaned_data.get("password1")
            response = ADWSCambiarClave(username, oldpassword, password)

            if response['CambiarClaveResult']:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                success = '<p class="text-success my-0">Contraseña actualizada correctamente.</p>'
                success += '<p class="text-success my-0">Para continuar inicia sesión nuevamente.</p>'
                messages.add_message(request, messages.SUCCESS, success)
                return redirect('/')
            else:
                msg = {msg: f"<p class='text-danger'>{response['Mensaje']}</p>"}
        else:
            msg = form.errors

    ## FIN CAMBIAR PASSWORD ##

    ### DIFUSIONES
    difusiones = Difusion.objects.all()

    context = {
        'recibos': recibos,
        'editForm':editForm,
        'passwordForm':passwordForm,
        'difusiones' : difusiones,
        'docente':docente_activo,
        'control':control,
        'msg':msg
    }
    return render(request, 'home/home.html', context)

@login_required
def ver_completo(request):
    recibos = []
    recibos_data = RDWSGetRecibosExt(request.user.datosadicionales.documento)
    if recibos_data is not None:
        for recibo in recibos_data:
            recibo = serialize_object(recibo)
            recibo.move_to_end('Id')
            recibo.move_to_end('Escalafon', False)
            #if recibo['Firmado'] and '-ANULADO-' not in recibo['Escalafon']:
            if True and '-ANULADO-' not in recibo['Escalafon']:
                recibos.append(recibo)

    return render(request, 'home/completo.html', {'recibos': recibos})

@login_required
def generate_nomade_pdf(request):
    service = request.POST['service']
    method = 'WSGEBIENESACARGO' if service == 'inventario' else 'WSGeFirmanteCta'

    filename = f'tmp/{request.user.username}_{service}.pdf'

    if os.path.exists(filename):
        pass
    else:
        data = NOMADEServices(request.user.datosadicionales.documento, method)
        if type(data) != bytes:
            msg = f'<p class="text-danger">{data}</p>'
            return JsonResponse({'msg':msg})
        else:
            with open(filename, 'wb') as f:
                f.write(codecs.decode(data, 'base64'))
                f.close()

    return JsonResponse({'msg':'success'})

@login_required
def view_nomade_pdf(request, title):

    filename = f'tmp/{title}.pdf'
    try:
        pdf = open(filename, "rb").read()

        return HttpResponse(pdf, content_type='application/pdf')
    except Exception as e:
        print(str(e))
        return render(request, 'layouts/404.html', status=404)

@login_required
def generate_pdf(request):
    id_recibo = request.POST['id_recibo']
    filename = 'tmp/{}.pdf'.format(request.user.username+'_'+id_recibo)
    if os.path.exists(filename):
        pass
    else:
        recibo = RDWSGetRecibo(id_recibo)
        with open(filename, 'wb' ) as f:
            f.write(recibo)

    return JsonResponse({'id':id_recibo})

@login_required
def view_pdf(request, id_recibo, periodo):
    filename = 'tmp/{}.pdf'.format(request.user.username+'_'+id_recibo)
    periodo = periodo.split("-")
    try:
        pdf = open(filename, "rb").read()
        addSystemLog(request.user, 5, " - " + periodo[1])

        return HttpResponse(pdf, content_type='application/pdf')
    except Exception as e:
        return render(request, 'layouts/404.html', status=404)

@login_required
def download_pdf(request, id_recibo, periodo):
    filename = 'tmp/{}.pdf'.format(request.user.username+'_'+id_recibo)
    try:
        response = FileResponse(open(filename, "rb"),as_attachment=True,filename=request.user.username+'_'+periodo+'.pdf')
        addSystemLog(request.user, 6, " - " + periodo)
        return response
    except Exception as e:
        return render(request, 'layouts/404.html', status=404)

@login_required
def enviar_mail(request):

    if request.user.datosadicionales.email is not None:
        id_recibo = request.POST['id_recibo']
        periodo = request.POST['periodo']
        anio = request.POST['anio']
        escalafon = request.POST['escalafon']

        if escalafon == 'ADMINISTRAC. CENTRAL':
            escalafon = 'SECO - ADMINISTRAC. CENTRAL'

        subject = 'Recibo Digital'
        text_content = 'Recibo Digital - Envío automático'
        from_email = 'Recibo de Sueldo Digital <{}>'.format(EMAIL_HOST_USER)
        to_email = request.user.datosadicionales.email
        imgs = ['mail-1.png','mail-2.png','mail-3.png','mail-4.png','mail-5.png','mail-6.png']

        context = {
            'usuario': request.user.datosadicionales.nombre+' '+request.user.datosadicionales.apellido,
            'periodo': periodo,
            'escalafon':escalafon,
            'anio':anio
        }

        t = get_template('layouts/mail.html')
        html = t.render(context)

        mail = EmailMultiAlternatives( subject, text_content, from_email, [to_email] )
        mail.attach_alternative( html, "text/html" )

        for f in imgs:
            fp = open('apps/static/assets/img/{}'.format(f), 'rb')
            mail_img = MIMEImage(fp.read())
            mail_img.add_header('Content-ID', '<{}>'.format(f))
            mail.attach(mail_img)

        try:
            mail.attach_file('tmp/{}_{}.pdf'.format(request.user.username, id_recibo))
        except:
            generate_pdf(request)
            mail.attach_file('tmp/{}_{}.pdf'.format(request.user.username, id_recibo))

        mail.send()
        addSystemLog(request.user, 7,' - {} - {}'.format(periodo,anio))

        msg = '<p class="text-success"> Recibo enviado exitosamente a {}</p>'.format(request.user.datosadicionales.email)
    else:
        msg = '<p class="text-danger"> Debe registrar un correo antes de enviar el recibo en editar datos. </p>'

    return JsonResponse({'msg': msg})

@login_required
def enviar_mail_banco(request):
    id_recibo = request.POST['id_recibo']
    periodo = request.POST['periodo']
    anio = request.POST['anio']
    escalafon = request.POST['escalafon']

    if escalafon == 'ADMINISTRAC. CENTRAL':
            escalafon = 'SECO - ADMINISTRAC. CENTRAL'

    nombre_apellido = request.user.datosadicionales.nombre + " " + request.user.datosadicionales.apellido

    subject = 'Recibo Digital de {} DNI {}'.format(nombre_apellido, request.user.datosadicionales.documento)
    text_content = 'Recibo Digital'
    from_email = 'Recibo de Sueldo Digital <{}>'.format(EMAIL_HOST_USER)

    # Mail de pruebas banco
    to_email = request.user.datosadicionales.email

    html = "<h3>Se adjunta recibo de {}, DNI número {}. Perteneciente al mes {} año {}, del escalafón {}</h3>".format(nombre_apellido, request.user.datosadicionales.documento,periodo, anio, escalafon )

    html += '<h4>Secretaría General, Legal y Técnica</h4>'
    html += '<h4>Secretaría de Gobierno Digital</h4>'

    mail = EmailMultiAlternatives( subject, text_content, from_email, [to_email] )
    mail.attach_alternative( html, "text/html" )

    try:
        mail.attach_file('tmp/{}_{}.pdf'.format(request.user.username, id_recibo))
    except:
        generate_pdf(request)
        mail.attach_file('tmp/{}_{}.pdf'.format(request.user.username, id_recibo))

    mail.send()
    addSystemLog(request.user, 8,' - {} - {}'.format(periodo,anio))

    msg = '<p class="text-success"> Recibo enviado exitosamente al Banco.</p>'
    return JsonResponse({'msg': msg})
