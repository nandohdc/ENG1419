# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from gpiozero import LED, Button
from gpiozero import LightSensor
from flask import Flask, render_template
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from requests import post
from threading import Timer



#variaveis
cliente = MongoClient("localhost", 27017)
banco = cliente["banco"]
colecao = banco["LEDS"]
chave = "dGYXAAcxb7TK0SZguXjU7d"
evento = "horario_leds"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave
timer = None

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

def obtem_tempo():
    data = datetime.now()-timedelta(minutes=1)
    minha_string =""
    tempo_leds = []
    for i in range (0,5):
        duracao = duracao_led(i,data)
        tempo_leds.append(duracao)
        minha_string = minha_string +str(duracao) +"|||"
    dados = {"value1": minha_string}
    print(minha_string)
    resultado = post(endereco, json=dados)
    print(resultado.text)
    return(tempo_leds)

def duracao_led(numLed,data):
    tempo_decorrido = timedelta(seconds=0)
    tempo_atual = datetime.now()
    ordenacao = [["horario", DESCENDING]]
    busca_maior = {"horario":{"$gt":data}}
    busca_menor = {"horario":{"$lt":data}}
    documento_maior = list(colecao.find(busca_maior, sort=ordenacao))
    documento_menor = colecao.find_one(busca_menor, sort=ordenacao)
    
    for doc in documento_maior:
        tempo_anterior = doc["horario"]
        if doc["estados"][numLed] == True:
            tempo_decorrido = tempo_decorrido + (tempo_atual - tempo_anterior)
        tempo_atual = tempo_anterior
    if documento_menor != None:
        if documento_menor["estados"][numLed] == True:
            tempo_decorrido = tempo_decorrido + (tempo_anterior - data)
    return tempo_decorrido.seconds


def timer_recorrente():
    print("Repetição")
    global timer
    timer = Timer(60, timer_recorrente)
    timer.start()
    obtem_tempo()
    return

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed = botao1_pressed
botoes[1].when_pressed = botao2_pressed
botoes[2].when_pressed = botao3_pressed
botoes[3].when_pressed = botao4_pressed
sensor_light = LightSensor(8)
sensor_light.when_light = desliga_LED4
sensor_light.when_dark = acende_LED4

timer_recorrente()


# rode o servidor
app.run(port=5000)

