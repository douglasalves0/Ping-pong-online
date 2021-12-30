import socket
import threading
import random
import json
from time import sleep

HOST = "localhost"

conexoes = []
jogadores_online = 0

x_rqt1 = 15
y_rqt1 = 330

x_rqt2 = 1045
y_rqt2 = 330

def recebendo(conn, cliente):

    global conexoes

    global x_rqt1
    global x_rqt2
    global y_rqt1
    global y_rqt2

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
                "y":y_rqt2
            }
        else:
            x_rqt2 = data["x"]
            y_rqt2 = data["y"]
            conn, cliente = conexoes[1]
            pack = {
                "x":x_rqt1,
                "y":y_rqt1
            }

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


