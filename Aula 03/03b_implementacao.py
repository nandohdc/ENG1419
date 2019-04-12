# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from Adafruit_CharLCD import Adafruit_CharLCD
from lirc import init, nextcode
from time import sleep


# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
init("aula", blocking=False)

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
        codigo = nextcode()
    return senha
                
            
# criação de componentes


# loop infinito
while True:
    lcd.clear()
    apt = coletar_digitos("Digite o apartamento")
    if validar_apartamento (apt):
        senha = coletar_digitos("Digite a senha")
        morador = retornar_nome_do_morador(apt,senha)
        if morador == None:
            lcd.clear()
            lcd.message("acesso negado")
        else:
            lcd.clear()
            lcd.message("Bem-vindo(a)\n" + morador)
    else:
        lcd.clear()
        lcd.message("apartamento \n invalido!")
    sleep(1)