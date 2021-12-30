import threading
import pygame
from pygame.locals import *
import tela_menu
from desenha import desenha
import constantes as const
from sys import exit
from sorteio import *
from raquete import *
from bola import *
from random import randint
from time import sleep
import socket
import json

x_rqt = -1
y_rqt = -1
player = 0
x2_rqt = -1
y2_rqt = -1
x_bola = -1
y_bola = -1
colidiu = False

def respondendo():

    global x_rqt
    global y_rqt

    global player

    global x2_rqt
    global y2_rqt

    global x_bola
    global y_bola

    global colidiu

    while(1):

        pack = {
            "player":player,
            "x":x_rqt,
            "y":y_rqt
        }

        tcp.send(json.dumps(pack).encode())
        data = json.loads(tcp.recv(1024).decode())
        x2_rqt = data["x"]
        y2_rqt = data["y"]
        x_bola = data["x_bola"]
        y_bola = data["y_bola"]
        if(not colidiu):
            colidiu = data["colidiu"]


def exibir_tela_online():

    global x_rqt
    global y_rqt
    global x2_rqt
    global y2_rqt
    global player
    global colidiu
    global x_bola
    global y_bola

    nome = ""
    while(len(nome) < 1 or len(nome) > 10):
        print("Maximo de caracteres: 10")
        print("Minimo de caracteres: 1")
        nome = input("Digite seu nome de jogador: ")
    
    ip = input("Digite o ip que deseja se conectar: ")
    porta = int(input("Digite a porta que deseja se conectar: "))

    global tcp 
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destino = (ip, porta)
    tcp.connect(destino)
    tcp.send(nome.encode())

    print("CONECTADO...")
    print("AGUARDANDO OUTROS JOGADORES...")

    #Esperando o servidor confirmar qual jogador você é
    mensagem = tcp.recv(1024).decode()
    print(mensagem)
    mensagem = json.loads(mensagem)
    tcp.send("{}".encode())

    player = int(mensagem["player"])
    
    x_rqt = int(mensagem["x"])
    y_rqt = int(mensagem["y"])

    limite_cima     = 120
    limite_baixo    = 530
    limite_direita  = 0
    limite_esquerda = 0

    if(player == 1):
        limite_direita  = 240
        limite_esquerda = 0
    else:
        limite_direita  = 1056
        limite_esquerda = 816

    print("VOCÊ É O PLAYER"+str(player))
    
    Respondendo = threading.Thread(target=respondendo)
    Respondendo.start()

    pygame.init()

    const.tela

    #DEFININDO A FONTE USADA PARA EXIBIR O PLACAR
    fonteTexto = pygame.font.SysFont(const.fonte, 18, True)
    fonteNumero = pygame.font.SysFont(const.fonte, 25, True)
    fonteAviso = pygame.font.SysFont(const.fonte, 45, True)

    imagem_seta = pygame.image.load(const.img_seta_direita)
    imagem_seta = pygame.transform.scale(imagem_seta, (32, 32))

    bola = pygame.image.load(const.img_bolinha)

    if(player == 1):
        raquete2 = pygame.image.load(const.img_raquete2)
        raquete = pygame.image.load(const.img_raquete1)
    else:
        raquete2 = pygame.image.load(const.img_raquete1)
        raquete = pygame.image.load(const.img_raquete2)

    som_raquete = pygame.mixer.Sound('sons/som_raquete.ogg')
    som_mesa = pygame.mixer.Sound('sons/som_mesa.ogg')
    som_aplausos = pygame.mixer.Sound('sons/som_aplausos.ogg')

    while True:
        
        const.relogio.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        
        desenha.desenha()

        tecla = pygame.key.get_pressed()

        #AÇÕES DO JOGADOR
        if tecla[K_w]:
            y_rqt = R_praCima(y_rqt, limite_cima)
        if tecla[K_a]:
            x_rqt = R_praEsquerda(x_rqt, limite_esquerda)
        if tecla[K_s]:
            y_rqt = R_praBaixo(y_rqt, limite_baixo)
        if tecla[K_d]:
            x_rqt = R_praDireita(x_rqt, limite_direita)

        if(colidiu):
            som_raquete.play()
            colidiu = False

        #ATUALIZANDO A POSIÇÃO DOS ELEMENTOS DO JOGO
        const.tela.blit(raquete, (x_rqt, y_rqt))
        const.tela.blit(raquete2,(x2_rqt, y2_rqt))
        const.tela.blit(bola, (x_bola, y_bola))
        pygame.display.flip()

        