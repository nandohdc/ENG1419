# importação de bibliotecas
from gpiozero import Button
from gpiozero import Buzzer
from requests import post, get
from os import system
from gpiozero import LED
from time import sleep
from subprocess import Popen
from Adafruit_CharLCD import Adafruit_CharLCD

# parâmetros iniciais do Telegram
chave = "644260839:AAHjHwJ59UjekUUu7aaRiPRd7aLYmxKsnsY"
endereco_base = "https://api.telegram.org/bot" + chave
endereco_enviar_mensagem = endereco_base + "/sendMessage"
id_da_conversa = "783030545"

# definição de funções
def mensagem_LCD():
    lcd.message("Gravando...")
    comando = ["arecord", "--duration", "5", "audio.wav"]
    aplicativo = Popen(comando)
    return

def fotos():
    for i in range(0,5):
        system("fswebcam --resolution 640x480 --skip 10 foto" + str(i) + ".jpg")
        led.blink(n=2, on_time=0.3, off_time=0.1)
    return

def mensagem():
    dados = {"chat_id": id_da_conversa, "text": "Abre a porta"}
    resposta_mensagem = post(endereco_enviar_mensagem, json=dados)
    return

# criação de componentes
botao = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)
led = LED(21)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

botao.when_pressed = mensagem_LCD
botao2.when_pressed = fotos
botao3.when_pressed = mensagem