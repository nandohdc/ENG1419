# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

# importação de bibliotecas
from gpiozero import Button
from gpiozero import Buzzer
from requests import post, get
from os import system
from gpiozero import LED
from time import sleep
from subprocess import Popen
from urllib.request import urlretrieve
from mplayer import Player
from gpiozero import DistanceSensor
from datetime import datetime, timedelta
from Adafruit_CharLCD import Adafruit_CharLCD
import unicodedata

# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")

# parâmetros iniciais do Telegram
chave = "644260839:AAHjHwJ59UjekUUu7aaRiPRd7aLYmxKsnsY"
id_da_conversa = "783030545"
endereco_base = "https://api.telegram.org/bot" + chave

# definição de funções
def liga_buzzer():
    buzzer.on()

def desliga_enviando_mensagem():
    buzzer.off()
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    dados = {"chat_id": id_da_conversa, "text": "Abre a porta", "reply_markup":{"keyboard":[["Abrir"], ["Soar Alarme"], ["Ignorar"]]}}
    arquivo = {"photo": open("foto.jpg", "rb")}
    dados_foto = {"chat_id": id_da_conversa, "text":"teste"}
    resposta_foto = post(endereco_enviar_foto, data=dados_foto, files=arquivo)
    resposta_mensagem = post(endereco_enviar_mensagem, json=dados)                
            
def grava_audio():
    global aplicativo
    comando = ["arecord", "--duration", "30", "audio.wav"]
    aplicativo = Popen(comando)
    
    return

def parar_gravacao():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
        system("opusenc audio.wav audio.ogg")
        arquivo = {"voice": open("audio.ogg", "rb")}
        dados_voice = {"chat_id": id_da_conversa}
        resposta_voice = post(endereco_enviar_voice, data=dados_voice, files=arquivo)
        print(resposta_voice.text)
    return

def chegou_na_porta():
    global atual
    atual = datetime.now()
    return 
    
def saiu_da_porta():
    global atual
    intervalo = timedelta(seconds=10)
    if (datetime.now() - atual > intervalo):
        dados = {"chat_id": id_da_conversa, "text": "Pessoa saiu."}
        resposta_mensagem = post(endereco_enviar_mensagem, json=dados)
            
        
    return

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)if unicodedata.category(c)!='Mn')

# criação de componentes
botao = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)
led = LED(21)
proximo_id_de_update = -1
atual = 0
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.10
aplicativo = None
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

base = "https://api.telegram.org/bot" + chave
endereco_enviar_mensagem = base + "/sendMessage"
endereco_enviar_foto = base + "/sendPhoto"
endereco_enviar_voice = base + "/sendVoice"
endereco_atualizacao = base + "/getUpdates"
endereco_download = base + "/getFile"

botao.when_pressed = liga_buzzer
botao.when_released = desliga_enviando_mensagem
botao2.when_pressed = led.off
botao3.when_pressed = grava_audio
botao3.when_released = parar_gravacao
sensor.when_in_range = chegou_na_porta
sensor.when_out_of_range = saiu_da_porta
player = Player()


#loop infinito
while True:
    dados = {"offset": proximo_id_de_update}
    resposta_atualizada = get(endereco_atualizacao, json=dados)
    dicionario_da_resposta = resposta_atualizada.json()
    for resultado in dicionario_da_resposta["result"]:
        mensagem = resultado["message"]
        if "text" in mensagem:
            texto = mensagem["text"]
            if texto == "Abrir":
                led.on()
            elif texto == "Soar Alarme":
                buzzer.beep(n=5, on_time=0.5, off_time=0.5)
            elif texto == "Ignorar":
                i = i + 1
            else:
                buzzer.beep(n=2, on_time=0.5, off_time=0.5)
                for i in range(0,2):
                    lcd.message("Mensagem \nRecebida!")
                    sleep(0.5)
                    lcd.clear()
                    sleep(0.5)
                texto = strip_accents(mensagem["text"])
                for i in range(0,len(texto)):
                    lcd.clear()
                    if(len(texto) > 16):
                        lcd.message(texto[i:i+16])
                    else:
                        lcd.message(texto)
                    sleep(0.5)
        elif "voice" in mensagem:
            print(mensagem)
            id_do_file = mensagem["voice"]["file_id"]
            dados_voice = {"file_id": id_do_file}
            resposta = get(endereco_download, json=dados_voice)
            dicionario=resposta.json()
            print(dicionario)
            final_do_link = dicionario["result"]["file_path"]
            print(final_do_link)
            link_do_arquivo = "https://api.telegram.org/file/bot"+chave+"/"+final_do_link
            arquivo_de_destino = "meu_arquivo.ogg"
            urlretrieve(link_do_arquivo, arquivo_de_destino)
            player.loadfile(arquivo_de_destino)
        elif "photo" in mensagem:
            foto = mensagem["photo"][-1]
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)


