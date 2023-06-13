import urllib3, requests, json, base64, xml.etree.ElementTree as ET

from zeep import Client
from zeep.transports import Transport
from apps.recibo.models import SistemLogs, TipoOperacion
from django.contrib.auth.models import User

session = requests.Session()
session.verify = False
transport = Transport(session=session)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


AD = Client('https://######', transport=transport)
RD = Client('http://######?wsdl', transport=transport)
MA = Client('http://######?wsdl', transport=transport)

NOMADE = 'https://######?wsdl'


def ADWSLogin(username, password):
    # verificacion del usuario con AD
    try:
        is_user = AD.service.Login(username, password)

        if is_user:
            return is_user
    except:
        return

def ADWSGetDni(username):
    # obtencion del documento del usuario
    try:
        dni = AD.service.GetDni(username)
        return dni
    except:
        return None

def ADWSGetUser(dni_usuario):
    try:
        usuario = AD.service.GetUser(dni_usuario)

        return usuario

    except:
        return 'No hay datos para el dni ' + dni_usuario

def ADWSGetUsuarioYPass(username):
    try:
        datos = AD.service.GetUsuarioYPass(username)
        return datos
    except:
        return None


#Cambio de clave de usuario
def ADWSCambiarClave(username, oldpassword, password):
    #obtención de usuario y clave
    try:
        datos = AD.service.CambiarClave(username, oldpassword, password)
        return datos
    except:
        return 'No se han encontrado datos del usuario ' + username

def RDWSGetRecibo(id_recibo):
    try:
        recibo = RD.service.GetRecibo(id_recibo)
        return recibo
    except:
        return None

def RDWSGetRecibosExt(dni_usuario):
    try:
        recibos = RD.service.GetRecibosFirmados(dni_usuario,0)
        return recibos
    except:
        return None

def NOMADEServices(dni_usuario,servicio):
    try:
        soap_body = f'''
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gen="Genexus">
            <soapenv:Header/>
            <soapenv:Body>
                <gen:ACPSWSAP.EXECUTE>
                    <gen:Wsdata>
                        <gen:ApiKey>?</gen:ApiKey>
                        <gen:SessionId>?</gen:SessionId>
                        <gen:Servicio>{servicio}</gen:Servicio>
                        <gen:Usuario>?</gen:Usuario>
                    </gen:Wsdata>
                    <gen:Parmin>
                        <gen:Parm><![CDATA[
                        {{"ProveDoc":{dni_usuario},
                        "ProveTipDoc":80,
                        "ProveClase":"G"}}
                        ]]></gen:Parm>
                    </gen:Parmin>
                </gen:ACPSWSAP.EXECUTE>
            </soapenv:Body>
            </soapenv:Envelope>
        '''
        # Encabezados de la solicitud SOAP
        headers = {"Content-Type": "text/xml;charset=UTF-8"}

        # Envía la solicitud SOAP al servicio web
        response = requests.post(NOMADE, data=soap_body, headers=headers)

        if response.status_code == 200:
            # Si la respuesta es exitosa, puedes obtener el contenido de la respuesta
            soap_response = response.content

            # Parsear el XML
            root = ET.fromstring(soap_response)

            parm_element = root.find('.//genexus:Parm', {'genexus':'Genexus'})
            parm_value = parm_element.text
            parm_dict = json.loads(parm_value)

            if parm_dict['ImportFileBase64'] != '':
                response = bytes(parm_dict['ImportFileBase64'],'utf-8')
            else:
                parm_element = root.find('.//genexus:Description', {'genexus':'GeneXus'})
                response = parm_element.text

            return response
        else:
            # Si la respuesta no es exitosa, puedes obtener el código de estado y el mensaje de error
            status_code = response.status_code
            error_message = response.text
            print(f"Error al llamar al servicio web. Código de estado: {status_code}. Mensaje: {error_message}")

    except Exception as e:
        return str(e)


def MAWSEsDocente(dni_usuario):
    try:
        data = MA.service.Execute(dni_usuario,'')
        return data
    except Exception as e:
        return None

def addSystemLog(usuario, tipo, detalle=''):

    tipo_operacion = TipoOperacion.objects.get(pk = tipo)

    if tipo == 2:
        log = SistemLogs(
            log_usuario=usuario,
            log_nombre= None,
            log_apellido= None,
            log_documento= None,
            log_tipo_operacion= tipo_operacion,
            log_operacion_detalle= tipo_operacion.__str__() + detalle
        )
    else:
        usuario = User.objects.get(username = usuario)
        log = SistemLogs(
            log_usuario=usuario.username,
            log_nombre=usuario.datosadicionales.nombre,
            log_apellido=usuario.datosadicionales.apellido,
            log_documento=usuario.datosadicionales.documento,
            log_tipo_operacion= tipo_operacion,
            log_operacion_detalle= tipo_operacion.__str__() + detalle
        )
    log.save()