# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS1
# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Buzzer
from lirc import init, nextcode
from time import sleep
from gpiozero import DistanceSensor
from datetime import datetime
from gpiozero import Button

from pymongo import ASCENDING, DESCENDING
# a linha abaixo apaga todo o banco e reinsere os moradores
#redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
colecao02 = banco["tentativas"]
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
buzzer = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.20
init("aula", blocking=False)
B1 = Button(11)

# definição de funções

def validar_apartamento(apt):
    doc = colecao.find_one({"apartamento": apt})
    if doc == None:
        return False
    else:
        return True

def retornar_nome_do_morador(apt, senha):
    doc = colecao.find_one({"apartamento": apt, "senha": senha})
    if doc == None:
        return None
    else:
        return doc["nome"]

def coletar_digitos(mensagem):
    lcd.clear()
    lcd.message(mensagem + "\n")
    codigo = nextcode()
    senha = ""
    while codigo != ["KEY_OK"]:
        if codigo != []:
            if codigo[0][-1] in "01234356789":
                senha += codigo[0][-1]
                lcd.message("*")
            buzzer.beep(n=1, on_time=0.3)
        codigo = nextcode()
    buzzer.beep(n=1, on_time=0.3)
    return senha

def principal ():
    lcd.clear()
    apt = coletar_digitos("Digite o apartamento")
    if validar_apartamento (apt):
        senha = coletar_digitos("Digite a senha")
        morador = retornar_nome_do_morador(apt,senha)
        if morador == None:
            lcd.clear()
            buzzer.beep(n=1, on_time=1.0)
            lcd.message("acesso negado")
        else:
            lcd.clear()
            lcd.message("Bem-vindo(a)\n" + morador)
        tentativas(apt,morador)
    else:
        lcd.clear()
        lcd.message("apartamento \n invalido!")
        
    

def tentativas (apt, name):
    if name == None:
        doc = {"apartamento":apt, "data":datetime.now()}
    else:
        doc = {"apartamento":apt, "data":datetime.now(), "nome": name}
    colecao02.insert(doc)
    return

def listar_tentativas():
    apt = coletar_digitos("Digite o apartamento")
    if validar_apartamento (apt):
        busca = {"apartamento":apt}
        orde = [["data", DESCENDING]]
        documentos = list(colecao02.find(busca,sort=orde))
        for doc in documentos:
            if "nome" in doc:
                n = doc["nome"]
            else:
                n = "SENHA INCORRETA"
            date_time = doc["data"].strftime("%d/%m/%Y (%H:%M:%S): ")
            print(date_time + n +"\n")
# criação de componentes


# loop infinito
sensor.when_in_range = principal
B1.when_pressed = listar_tentativas 
