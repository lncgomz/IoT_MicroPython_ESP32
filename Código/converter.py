from machine import Pin, PWM #Manejo de Pines del ESP32 y Pulse Width Modulation
from time import sleep #Manejo de pausas en tiempo de ejecución
import time #Manejo del temporizador

red = PWM(Pin(25), 5000) #Pin Rojo en el LED RGB
green = PWM(Pin(26), 5000) #Pin Verde en el LED RGB
blue = PWM(Pin(27), 5000) #Pin Azul en el LED RGB
tu = 125 #Parámetro de Unidad de Tiempo (Time Unit) para implementación del Código Morse
freq = 1500 #Parámetro de Frecuencia del beep para implementación del Código Morse

#Definición de Pines para manejo del display 7 Segmentos
a = Pin(15, Pin.OUT)
b = Pin(2, Pin.OUT)
c = Pin(4, Pin.OUT)
d = Pin(5, Pin.OUT)
e = Pin(18, Pin.OUT)
f = Pin(19, Pin.OUT)
g = Pin(21, Pin.OUT)
dp = Pin(22, Pin.OUT)

#Mapeo de Letras a código RGB
#Mapeo basado en la información disponible en
#http://www.christianfaur.com/conceptual/colorAlphabet/image3.html

colors = {'A': [0,0,180],  #Azul
          'B': [175, 13,102], #Rojo-Violeta
          'C': [146, 248,70], #Verde-Amarillo
          'D': [255,200,47],      #Amarillo-Naranja
          'E': [255,118,0], #Anaranjado
          'F': [185,185,185], #Gris Claro
          'G': [235,235,222], #Blanco Tenue
          'H': [100,100,100],      #Gris
          'I': [255,255,0], #Amarillo
          'J': [55,19,112], #Violeta Oscuro
          'K': [255,255,150], #Amarillo Claro
          'L': [202,62,94],      #Rosado Oscuro
          'M': [205,145,63],    #Anaranjado Oscuro
          'N': [12,75,100],  #Verde Azulado
          'O': [255,0,0],  #Rojo
          'P': [175,155,50], #Amarillo Oscuro
          'Q': [100,100,100], #Gris Oscuro
          'R': [37,70,25], #Verde Oscuro
          'S': [121,33,135], #Púrpura
          'T': [83,140,208], #Azul Claro
          'U': [0,154,37], #Verde,
          'V': [178,220,205], #Cyan,
          'W':[255,152,213], #Rosado,
          'X':[0,0,74], #Azul Oscuro,
          'Y':[175,200,74], #Verde Oliva,
          'Z':[63,25,12]} #Café Rojizo

#Mapeo de Letras a código Morse
#Mapeo basado en la información disponible en
#https://es.wikipedia.org/wiki/C%C3%B3digo_morse

morse =  {'A': [0,1],  
          'B':[1,0,0,0],
          'C':[1,0,1,0],
          'D': [1,0,0],
          'E': [0],
          'F': [0,0,1,0],
          'G': [1,1,0],
          'H': [0,0,0,0],
          'I': [0,0],
          'J': [0,1,1,1],
          'K': [1,0,1],
          'L': [0,1,0,0],      
          'M': [1,1],   
          'N': [1,0],  
          'O': [1,1,1],
          'P': [0,1,1,0],
          'Q': [1,1,0,1],
          'R': [0,1,0],
          'S': [0,0,0],
          'T': [1],
          'U': [0,0,1],
          'V': [0,0,0,1],
          'W': [0,1,1],
          'X': [1,0,0,1],
          'Y': [1,0,1,1],
          'Z': [1,1,0,0]}  

#Mapeo de Letras a representación en 7 segmentos
#Mapeo basado en la información disponible en
#https://en.wikichip.org/wiki/seven-segment_display/representing_letters

letters =  {'A': '11101110',
            'B': '00111110',
            'C': '10011100',
            'D': '11111000',
            'E': '10011110',
            'F': '10001110',
            'G': '10111100',
            'H': '01101110',
            'I': '00001100',
            'J': '01111000',
            'K': '10101110',
            'L': '00011100',      
            'M': '11010100',    
            'N': '11101100',  
            'O': '11111100',
            'P': '11001110',
            'Q': '11111101',
            'R': '00001010',
            'S': '10110110',
            'T': '00011110',
            'U': '01111100',
            'V': '01010100',
            'W': '01111110',
            'X': '10010010',
            'Y': '01001110',
            'Z': '11011010'
            }  


#Función para convertir un mensaje de texto en Código RGB

def text2Color(text):
    characters = list(text) #Se descompone el texto en un arreglo de letras
    for c in characters: # Se itera sobre cada una de las letras (y espacios) de la palabra
        if c.upper() in colors: #Se verifica que la letra seleccionada pertenezca al diccionario 
            color = colors[c.upper()] #Se busca el código RGB correspondiente a la letra en cuestión
            print(c.upper()) #Se imprime la letra evaluada (Debugging)
            print(color) # Se imprime el código RGB correspondiente (Debugging)
            text2SevenSeg(c) #Se representa la letra evaluada en el display 7 segmentos
            red.duty(color[0]) #Se asigna el valor R del código RGB al Duty Cycle del pin correspondiente
            green.duty(color[1]) #Se asigna el valor G del código RGB al Duty Cycle del pin correspondiente
            blue.duty(color[2]) #Se asigna el valor B del código RGB al Duty Cycle del pin correspondiente
            sleep(1) #Pausa de 1 segundo entre letra y letra
        else: #Si la letra no está en el diccionario (Espacio, Número, Ñ)
            turnOffDisplay() # se apaga el display 7 segmentos
            # Así como el LED RGB
            red.duty(0)
            green.duty(0)
            blue.duty(0)
            sleep(2) #Y se hace una pausa de 2 segundos
    #Al terminar la iteración, se apaga el LED RGB
    red.duty(0)
    green.duty(0)
    blue.duty(0)
    turnOffDisplay() #Y el display 7 segmentos

#Función para convertir un mensaje de texto en Código Morse
    
def text2Morse(text):
    characters = list(text) #Se descompone el texto en un arreglo de letras
    for c in characters: # Se itera sobre cada una de las letras (y espacios) de la palabra
        if c.upper() in morse: #Se verifica que la letra seleccionada pertenezca al diccionario 
            m = morse[c.upper()] #Se busca el código Morse correspondiente a la letra en cuestión
            print(c.upper()) #Se imprime la letra evaluada (Debugging)
            print(m) # Se imprime el código Morse correspondiente (Debugging)
            text2SevenSeg(c) #Se representa la letra evaluada en el display 7 segmentos
            for letter in m: #Por cada símbolo en el código morse correspondiente
                if letter == 0: #El cero representa el punto
                    tone = PWM(Pin(33), freq=int(freq), duty=512) #Se define al Pin33 como manejador del Buzzer
                    time.sleep(tu*0.001) # Se emite un beep corto
                    tone.deinit() # Se apaga el buzzer
                    time.sleep(tu*0.001) # Y se define una pausa corta entre letras
                else: # El 1 representa la raya
                    tone = PWM(Pin(33), freq=int(freq), duty=512) #Se define al Pin33 como manejador del Buzzer
                    time.sleep(3*tu*0.001) # Se emite un beep largo (3 veces la duración del punto)
                    tone.deinit() # Se apaga el buzzer
                    time.sleep(tu*0.001) # Y se define una pausa corta entre letras                
        else: #Si la letra no está en el diccionario (Espacio, Número, Ñ)
            tone = PWM(Pin(33), freq=int(0), duty=512) #Se define al Pin33 como manejador del Buzzer
            tone.deinit() # Se apaga el buzzer
            turnOffDisplay() #Se apaga el display de 7 segmentos
            time.sleep(3*tu*0.001) # Y se define una pausa larga
    turnOffDisplay() #Una vez terminada la iteración, se apaga el display 7 segmentos

#Función para representar una letra en el display 7 segmentos
    
def text2SevenSeg(msg): 
    characters = list(msg) #Se descompone el texto en un arreglo de letras
    for ch in characters: # Se itera sobre cada una de las letras (y espacios) de la palabra
        if ch.upper() in letters: #Se verifica que la letra seleccionada pertenezca al diccionario             
            segs = list(letters[ch.upper()]) #Se busca el código 7Seg correspondiente a la letra en cuestión
            #Y se asigna cada letra del código al segmento correspondiente en el display
            a.value(int(segs[0]))
            b.value(int(segs[1]))
            c.value(int(segs[2]))
            d.value(int(segs[3]))
            e.value(int(segs[4]))
            f.value(int(segs[5]))
            g.value(int(segs[6]))
            dp.value(0) #Punto decimal siempre apagado
            sleep(1) #Pausa de 1 segundo
        else: #Si la letra no está en el diccionario (Espacio, Número, Ñ)
            turnOffDisplay() #Se apaga el display
            sleep(2) #Y se hace una pausa de 2 segundos

# Función para apagar el display de 7 segmentos (Todos los segmentos apagados)
def turnOffDisplay():
    a.value(0)
    b.value(0)
    c.value(0)
    d.value(0)
    e.value(0)
    f.value(0)
    g.value(0)
    dp.value(0)

# Función de para generar la sección dinámica de la página web de respuesta después de recibir una solicitud

def generateResponseWebPage(message, mode):
    response = ''
    if (mode == 1):  #El usuario seleccionó Conversión a Código RGB
        characters = list(message) #Se descompone el texto en un arreglo de letras
        for ch in characters: # Se itera sobre cada una de las letras (y espacios) de la palabra
            if ch.upper() in colors: #Se verifica que la letra seleccionada pertenezca al diccionario 
                color = colors[ch.upper()] #Se busca el código RGB correspondiente a la letra en cuestión
                #y se genera una fila con los valores de la letra y su representación en código RGB
                #La celda con el código RGB está coloreada con el color que está representando
                response = response + "<tr><td>" + ch.upper() + """</td><td style="color:rgb(""" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + """)">""" + str(color) + "</td></tr>"
            else: #Si la letra no se encuentra en el diccionario, se representa como 3 rayas (---)
               response = response + "<tr><td>" + ch.upper() + "</td><td>---</td></tr>"
    else: #El usuario seleccionó Conversión a Código Morse
        characters = list(message) #Se descompone el texto en un arreglo de letras
        for ch in characters: # Se itera sobre cada una de las letras (y espacios) de la palabra
            if ch.upper() in morse: #Se verifica que la letra seleccionada pertenezca al diccionario 
                m = str(morse[ch.upper()]) #Se busca el código Morse correspondiente a la letra en cuestión
                m = m.replace('0', '.') #Se reemplaza el 0 con el punto (.)
                m = m.replace('1','-') #Y el 1 con la raya (-)
                m = m.replace(',', '') #Se eliminan las comas
                #y se genera una fila con los valores de la letra y su representación en código RGB
                response += "<tr><td>" + ch.upper() + "</td><td>" + m + "</td></tr>" 
            else:
                #Si la letra no se encuentra en el diccionario, se representa como 3 rayas (---)
               response += "<tr><td>" + ch.upper() + "</td><td>---</td></tr>"
    return response
    

      
            
    
