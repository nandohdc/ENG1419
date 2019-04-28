# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from gpiozero import LED, Button
from gpiozero import LightSensor
from flask import Flask, render_template
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta



#variaveis
cliente = MongoClient("localhost", 27017)
banco = cliente["banco"]
colecao = banco["LEDS"]


# criação do servidor
app = Flask(__name__)

@app.route("/")
def lista_leds():
    ordenacao = [["horario", DESCENDING]]
    documento = colecao.find_one(sort=ordenacao)
    print(documento)
    states = documento["estados"]
    return render_template("index.html", data=states)
    

# definição de funções das páginas
@app.route("/luz/<int:x>/<string:modo>")
def mostrar_inicio(x,modo):
    print(x)
    print(modo)
    if modo == "on":
        leds[x].on()
    elif modo == "off":
        leds[x].off()
    
    salva_horarios()
    return "Bem-vindo!"

def botao1_pressed():
    leds[0].toggle()
    salva_horarios()
    return

def botao2_pressed():
    leds[1].toggle()
    salva_horarios()
    return

def botao3_pressed():
    leds[2].toggle()
    salva_horarios()
    return

def botao4_pressed():
    leds[3].toggle()
    salva_horarios()
    return

def salva_horarios():
    horario = datetime.now()
    state = []
    for led in leds:
        state.append(led.is_lit)
    dados={"horario":horario, "estados":state}
    colecao.insert(dados)
    return

def desliga_LED4():
    leds[4].off()
    salva_horarios()
    return

def acende_LED4():
    leds[4].on()
    salva_horarios()
    return


    

# criação dos componentes
leds = [LED(21, active_high=False), LED(22, active_high=False), LED(23, active_high=False), LED(24, active_high=False), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed = botao1_pressed
botoes[1].when_pressed = botao2_pressed
botoes[2].when_pressed = botao3_pressed
botoes[3].when_pressed = botao4_pressed
sensor_light = LightSensor(8)
sensor_light.when_light = desliga_LED4
sensor_light.when_dark = acende_LED4



# rode o servidor
app.run(port=5000)
