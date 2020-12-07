import converter

# Función de para generar la página web dinámica de respuesta después de recibir una solicitud

def generateResponse(message, mode):
    resultRows = converter.generateResponseWebPage(message, mode) #Se genera la sección dinámica de la página
    strMode = '' #Se inicializa la variable que representa el modo de conversión seleccionado (1: Código RGB / 0: Código Morse)
    if mode == 1:
        strMode = "C&oacute;digo RGB"
    else:
        strMode = "C&oacute;digo Morse"
    # Y se genera el código html con la sección dinámica y el modo de conversión incluídos
    html = """<html><head><title>Proyecto IoT MicroPython UdeA</title><meta name="viewport" content="width=device-width,initial-scale=1">
            <link rel="icon" href="data:,"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
            crossorigin="anonymous"><style>html {font-family: Helvetica;display: inline-block;margin: 0px auto;text-align: center;}
            h1 {color: #01602D;padding: 0;margin-top: 1px;margin-bottom: 1px;}li {text-align: left;}th, td {margin-left: 10px;text-align: center}
            </style></head><body><div class="container"><img src="https://www.pngfind.com/pngs/m/230-2301392_python-vector-head-white-python-logo-png-transparent.png"alt="MicroPython"width="50" height="50">
            <h1>Resultados</h1><div><ul><li>Mensaje Enviado: """ + str(message) + "</li><li>Modo de Conversi&oacute;n Seleccionado: " + str(strMode) + "</li></ul></div><table><tr><th>Letra</th><th>Valor</th></tr>" + str(resultRows) + "</table></body></html>"
    return html


