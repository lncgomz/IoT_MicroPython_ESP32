# Proyecto Final IoT: Curso de Python UdeA

# Proyecto realizado por:
# Leoncio Gómez

#Importar librerías
import wifimgr  #Manejo de Conexión WiFi
import machine  #Manejo de componentes del ESP32
import ure     #Manejo de direcciones URL
import converter #Convertidor de mensajes enviados a través de la página web en señales de luz o sonido
import responsePage #Página web de respuesta dinámica

# Creación de Socket para conexión a WiFi
try:
  import usocket as socket
except:
  import socket
wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass
print("ESP OK")

def web_page():  # Página de inicio que se muestra al conectarse al ESP32
    
  html = """<html>
 <head>
 <title>Proyecto IoT MicroPython UdeA</title><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
 integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"><style>
 html {
 font-family: Helvetica;display: inline-block;margin: 0px auto;
 text-align: center;
 }h1 {
 color: #01602D;
 padding: 0;
 margin-top: 1px;
 margin-bottom: 1px;
 }p {
 font-size: 1.5rem;
 }a {
 color: white;
 }.info {
 background: #fffbce;text-align: center;
 margin-top: 20px;
 }.footer {
 background-color: #01602D;position: fixed;
 bottom: 0; margin-bottom:5px; width: 100%;
 }.footerTextCenter {
 text-align: center;
 color: #ffffff
 }input[type='radio']:after {width: 15px;
 height: 15px;
 border-radius: 15px;top: 0px;
 left: -1px;
 position: relative;
 background-color: #d1d3d1;content: '';
 display: inline-block;visibility: visible;border: 2px solid #01602D;}input[type='radio']:checked:after {width: 15px;
 height: 15px;
 border-radius: 15px;top: 0px;
 left: -1px;
 position: relative;
 background-color: #01602D;content: '';
 display: inline-block;visibility: visible;border: 2px solid white;}</style>
 </head>
 <body>
 <div class="container"><img src="https://www.pngfind.com/pngs/m/230-2301392_python-vector-head-white-python-logo-png-transparent.png"
 alt="MicroPython" width="50" height="50"><h1>Proyecto IoT MicroPython</h1><h1>UdeA</h1>
 <div class="info">
 <p>Introduzca el texto en el recuadro e indique si desea verlo convertido en <b>C&oacute;digo de Colores</b> o en <b>C&oacute;digo Morse</b>
 </br>para una mejor experiencia, se recomienda <u>utilizar s&oacute;lamente caracteres alfab&eacute;ticos, omitiendo
 acentos y la letra &Ntilde;</u></p></div><form name="myform" action="" method="GET">Escriba aqu&iacute; su mensaje:<br><input name="msg"
 name="msg" VALUE=""><P><div role="radiogroup"><input role="radio" type="radio" id="mode" name="mode" value="1" aria-checked="true"
 checked="checked"> Convertir a Colores<br><input role="radio" type="radio" id="mode" name="mode" value="0" aria-checked="false"> Convertir
 a Morse<br></div><br><input type="submit" name="button" Value="Enviar"></form>
 <div class="container row footer footerText"><div class="col-md-12 col-sm-12 col-lg-12 footerTextCenter"><u>Elaborado por:</u>
 <a href="https://github.com/lncgomz">Leoncio G&oacute;mez - Diciembre 2020</a></div></div></body></html>"""

  return html

# Función para la creación de página web dinámica de respuesta
def response_web(message, mode):
    return responsePage.generateResponse(message, mode)

# Función para enviar la página web dinámica de respuesta al usuario
def sendResult(message, mode):
    response = response_web(message, mode)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  
# Inicialización del Socket
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()

#Bucle infinito para 'escuchar' peticiones de conexión
while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Conexión recibida desde %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    try:
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(0).decode("utf-8").rstrip("/") #Filtrado de peticiones GET/POST
    except Exception:
        url = None
    if url is not None:
        match = ure.search("msg=([^&]*)&mode=([^&]*)", url) #La página web inicial envía dos parámetros vía GET (msg: Mensaje y mode: RGB(1) o Morse(0))
        if match is not None:
            msg = match.group(1).replace('msg=','')
            msg = msg.replace('+',' ')
            md = match.group(2).replace('mode=','') 
            if (int(md) == 1): # Modo = 1 : Conversión de Código RGB
                sendResult(msg, 1) # Crear página web dinámica de respuesta
                converter.text2Color(msg) # Convertir mensaje a código RGB
                
            else: # Modo = 0 : Conversión de Código Morse
                sendResult(msg, 0) # Crear página web dinámica de respuesta
                converter.text2Morse(msg) # Convertir mensaje a código RGB
                
    # Si no se ha enviado una petición GET/POST mostrar página de inicio
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
