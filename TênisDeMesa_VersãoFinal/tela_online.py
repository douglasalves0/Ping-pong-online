import threading
import pygame, tela_menu
from desenha import desenha
import constantes as const
from pygame.locals import *
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

def esperando():
    
    #Vai esperar:
    #   -colisões
    #   -posição da bola
    #   -posição da outra raquete
    #   -pontuação1/pontuação2
    #   -sets1/sets2
    #   -se o jogo acabou ou não
    
    global x2_rqt
    global y2_rqt

    while(1):    
        data = json.loads(tcp.recv(1024).decode())
        x2_rqt = data["x"]
        y2_rqt = data["y"]
        print(data)

def respondendo():

    global x_rqt
    global y_rqt
    global player

    while(1):

        pack = {
            "posx":x_rqt,
            "posy":y_rqt
        }

        tcp.send(json.dumps(pack).encode())
        sleep(0.05)


def exibir_tela_online():

    global x_rqt
    global y_rqt
    global x2_rqt
    global y2_rqt
    global player

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
    mensagem = json.loads(tcp.recv(1024).decode())

    player = int(mensagem["player"])
    
    x_rqt = int(mensagem["posx"])
    y_rqt = int(mensagem["posy"])

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

    Esperando = threading.Thread(target=esperando)
    Esperando.start()
    
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

    #CRIAÇÃO DE MÁSCARAS PARA VERIFICAR COLISÕES ENTRE AS IMAGENS
    mascara_bola = pygame.mask.from_surface(bola)
    mascara_rqt = pygame.mask.from_surface(raquete)

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

        #ATUALIZANDO A POSIÇÃO DOS ELEMENTOS DO JOGO
        const.tela.blit(raquete, (x_rqt, y_rqt))
        const.tela.blit(raquete2,(x2_rqt, y2_rqt))
        pygame.display.flip()

        