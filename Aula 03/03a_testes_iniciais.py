# importação de bibliotecas
from gpiozero import Button
from gpiozero import Buzzer
from gpiozero import DistanceSensor
from gpiozero import LED
from Adafruit_CharLCD import Adafruit_CharLCD
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

# definição de funções
def toca_campainha():
    buzzer.beep(n=1, on_time=0.5)
    return

def pisque ():
    led.blink(n=2, on_time=0.5, off_time=0.5)

def medir ():
    lcd.clear()
    distancia = sensor.distance*100
    lcd.message("%.1f" % distancia)
    doc = {"distancia":distancia, "data":datetime.now()}
    colecao.insert(doc)
    return


# criação de componentes
B1 = Button(11)
B2 = Button(12)
buzzer = Buzzer(16)
led = LED(21)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.10
cliente = MongoClient("localhost", 27017)
banco = cliente["testes-iniciais"]
colecao = banco["distancias"]


B1.when_pressed = toca_campainha
B2.when_pressed = medir
sensor.when_in_range = pisque
sensor.when_out_of_range = pisque