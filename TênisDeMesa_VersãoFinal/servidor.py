import socket
import threading
import random
import json
from time import sleep
import constantes as const
import pygame
import random

HOST = "localhost"

conexoes = []
jogadores_online = 0

x_rqt1 = 15
y_rqt1 = 330

x_rqt2 = 1045
y_rqt2 = 330

colidiu1 = False
colidiu2 = False

sets_jogador1 = 0
sets_jogador2 = 0

pts_jogador1 = 0
pts_jogador2 = 0

pontos = 0

vencedor = ""

controlar_saque = True
atrasar_saque = False
contou_ponto = False
acabou_set = False
direita = False
esquerda = False
v_x_bolinha = 0
v_y_bolinha = 0

posicao_seta = []

if random.randint(0, 1) == 0:
    posicao_seta = [850, 15]
else:
    posicao_seta = [850, 55]

posicao_saque = []

if posicao_seta == [850, 15]:
    posicao_saque = [92, 359]
else:
    posicao_saque = [1005, 359]

x_bola = posicao_saque[0]
y_bola = posicao_saque[1]

def recebendo(conn, cliente):

    global conexoes

    global x_rqt1
    global x_rqt2
    global y_rqt1
    global y_rqt2

    global colidiu1
    global colidiu2

    while(1):

        data = json.loads(conn.recv(1024).decode())
        conn, cliente = (0,0)
        pack = {}

        if(data["player"] == 1):
            x_rqt1 = data["x"]
            y_rqt1 = data["y"]
            conn, cliente = conexoes[0]
            pack = {
                "x":x_rqt2,
                "y":y_rqt2,
                "colidiu": colidiu1,
                "x_bola":x_bola,
                "y_bola":y_bola
            }
            if(colidiu1):
                colidiu1 = False
        else:
            x_rqt2 = data["x"]
            y_rqt2 = data["y"]
            conn, cliente = conexoes[1]
            pack = {
                "x":x_rqt1,
                "y":y_rqt1,
                "colidiu": colidiu2,
                "x_bola":x_bola,
                "y_bola":y_bola
            }
            if(colidiu2):
                colidiu2 = False



        conn.send(json.dumps(pack).encode())


PORT = int(input("Digite a porta em que deseja abrir o servidor: "))

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (HOST, PORT)
tcp.bind(origem)
tcp.listen(5)
print(f"CONECTADO COM SUCESSO A {HOST}:{PORT}")

while(jogadores_online < 2):
    conn, cliente = tcp.accept()
    nome = conn.recv(1024).decode()
    if(nome.startswith("SSH") or nome == ""):
        print("TENTATIVA DE CONEXÃO DO NGROK BLOQUEADA")
        continue
    print("CONECTADO COM SUCESSO A <" + nome + ">.")
    conexoes.append((conn,cliente))
    jogadores_online+=1

#começa a tratar dos problemas do cliente
for i in range(len(conexoes)):

    posx = -1
    posy = -1

    if(i+1 == 1):
        posx = x_rqt1
        posy = y_rqt1
    else:
        posx = x_rqt2
        posy = y_rqt2

    envio = {
        "player":i+1,
        "x":posx,
        "y":posy
    }

    conn, cliente = conexoes[i]
    
    conn.send(json.dumps(envio).encode())
    conn.recv(1024).decode()

    t = threading.Thread(target=recebendo, args=(conn, cliente))
    t.start()

bola = pygame.image.load(const.img_bolinha)
raquete1 = pygame.image.load(const.img_raquete1)
raquete2 = pygame.image.load(const.img_raquete2)

#CRIAÇÃO DE MÁSCARAS PARA VERIFICAR COLISÕES ENTRE AS IMAGENS
mascara_bola = pygame.mask.from_surface(bola)
mascara_rqt1 = pygame.mask.from_surface(raquete1)
mascara_rqt2 = pygame.mask.from_surface(raquete2)

while True:#Simulando o jogo

    const.relogio.tick(30)
    #RETORNA A POSIÇÃO DA BOLINHA EM RELAÇÃO ÀS RAQUETES
    sobreposicao1 = (x_bola - x_rqt1, y_bola - y_rqt1)
    sobreposicao2 = (x_bola - x_rqt2, y_bola - y_rqt2)

    #A FUNÇÃO OVERLAP RETORNA O PONTO DE INTERSEÇÃO
    #DO PRIMEIRO PARÂMETRO QUE É UMA
    #MÁSCARA E O DESLOCAMENTO DA SEGUNDA IMAGEM
    colisao1 = mascara_rqt1.overlap(mascara_bola, sobreposicao1)
    colisao2 = mascara_rqt2.overlap(mascara_bola, sobreposicao2)

    #MOVIMENTANDO A BOLINHA A PARTIR DA COLISÃO DA BOLINHA COM UMA RAQUETE
    if colisao1 or colisao2:

        colidiu2 = True
        colidiu1 = True

        v_x_bolinha = random.randint(2, 3)
        v_y_bolinha = random.randint(-1, 1)
        
        if colisao1:
            direita = True
            esquerda = False

        if colisao2:
            direita = False
            esquerda = True
            
    if direita:
        x_bola += v_x_bolinha
    if esquerda:
        x_bola -= v_x_bolinha
    
    y_bola += v_y_bolinha

    #VERIFICANDO SE A BOLINHA PASSOU DOS LIMITES DA TELA

    if x_bola < -32 or x_bola > 1130:
        contou_ponto = True
        controlar_saque = True
        atrasar_saque = True
        direita = False
        esquerda = False

        x_rqt1 = 15
        y_rqt1 = 330

        x_rqt2 = 1045
        y_rqt2 = 330

        if x_bola > 1130:
            pts_jogador1 += 1
            v_y_bolinha = 0
            x_bola = posicao_saque[0]
            y_bola = posicao_saque[1]

        if x_bola < -32:
            pts_jogador2 += 1
            v_y_bolinha = 0
            x_bola = posicao_saque[0]
            y_bola = posicao_saque[1]

    #VERIFICANDO SE A BOLINHA ALCANÇOU AS BORDAS SUPERIOR E INFERIOR DA MESA
    if(y_bola < 130):
        y_bola = 130
        v_y_bolinha = -v_y_bolinha

    if(y_bola > 585):
        y_bola = 585
        v_y_bolinha = -v_y_bolinha
