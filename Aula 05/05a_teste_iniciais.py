# importação de bibliotecas
from gpiozero import LED
from gpiozero import MotionSensor
from threading import Timer
from gpiozero import LightSensor
from gpiozero import Button
from gpiozero import DistanceSensor
from requests import post

#variaveis
led = [LED(21),LED(22)] 
sensor = MotionSensor(27)
sensor_light = LightSensor(8)
botao = Button(11)
sensor_distance = DistanceSensor(trigger=17, echo=18)
timer = None
chave = "dGYXAAcxb7TK0SZguXjU7d"
evento = "google_docs"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave

# definição de funções
def detecta_movimento():
    led[0].on()
    led[1].on()
    parar_timer()
    return

def detecta_inercia():
    led[0].off()
    timer_recorrente()
    return

def timer_recorrente():
    print("Repetição")
    global timer
    timer = Timer(8.0, led[1].off)
    timer.start()
    return
    
def parar_timer():
    global timer
    if timer != None:
        timer.cancel()
        timer = None
    return

def applet_evento():
    dados = {"value1":  (sensor_light.value*100), "value2":   (sensor_distance.distance*100)}
    resultado = post(endereco, json=dados)
    print(resultado.text)
    return

sensor.when_motion = detecta_movimento
sensor.when_no_motion = detecta_inercia
botao.when_pressed = applet_evento

# criação de componentes


# loop infinito
