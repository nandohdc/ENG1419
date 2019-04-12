# importação de bibliotecas
from os import system


# importação de bibliotecas
from gpiozero import Button
from gpiozero import Buzzer
from requests import post, get
from os import system
from gpiozero import LED
from time import sleep

# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")

# parâmetros iniciais do Telegram
chave = "644260839:AAHjHwJ59UjekUUu7aaRiPRd7aLYmxKsnsY"
id_da_conversa = "40985105"
endereco_base = "https://api.telegram.org/bot" + chave

# definição de funções
def liga_buzzer():
    buzzer.on()

def desliga_enviando_mensagem():
    buzzer.off()
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    dados = {"chat_id": id_da_conversa, "text": "Abre a porta"}
    arquivo = {"photo": open("foto.jpg", "rb")}
    dados_foto = {"chat_id": id_da_conversa, "text":"teste"}
    resposta_foto = post(endereco_enviar_foto, data=dados_foto, files=arquivo)
    resposta_mensagem = post(endereco_enviar_mensagem, json=dados)                
            
##    print(resposta_mensagem.text)
##    print(resposta_foto.text)

# criação de componentes
botao = Button(11)
botao2 = Button(12)
buzzer = Buzzer(16)
led = LED(21)
proximo_id_de_update = -1

base = "https://api.telegram.org/bot" + chave
endereco_enviar_mensagem = base + "/sendMessage"
endereco_enviar_foto = base + "/sendPhoto"
endereco_atualizacao = base + "/getUpdates"

botao.when_pressed = liga_buzzer
botao.when_released = desliga_enviando_mensagem
botao2.when_pressed = led.off

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
            elif texto == "Alarme":
                buzzer.beep(n=5, on_time=0.5, off_time=0.5)
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)



# parâmetros iniciais do Telegram
chave = "COLOQUE A SUA CHAVE AQUI!"
id_da_conversa = "COLOQUE O ID DA SUA CONVERSA AQUI!"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções


# criação de componentes


# loop infinito
