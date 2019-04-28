# importação de bibliotecas
from gpiozero import LED, Button
from gpiozero import LightSensor
from flask import Flask




# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
@app.route("/luz/<int:x>/<string:modo>")
def mostrar_inicio(x,modo):
    print(x)
    print(modo)
    if modo == "on":
        leds[x].on()
    elif modo == "off":
        leds[x].off()
    return "Bem-vindo!"



def botao1_pressed():
    leds[0].toggle()
    return

def botao2_pressed():
    leds[1].toggle()
    return

def botao3_pressed():
    leds[2].toggle()
    return

def botao4_pressed():
    leds[3].toggle()
    return
# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed = botao1_pressed
botoes[1].when_pressed = botao2_pressed
botoes[2].when_pressed = botao3_pressed
botoes[3].when_pressed = botao4_pressed
sensor_light = LightSensor(8)
sensor_light.when_light = leds[4].off
sensor_light.when_dark = leds[4].on




# rode o servidor
app.run(port=5000)