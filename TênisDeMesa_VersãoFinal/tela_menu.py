import pygame, tela_multijogador, tela_treinamento, tela_regras, tela_online
import constantes as const
from sys import exit
from pygame.locals import *
from sorteio import *
from time import sleep

def exibir_tela_menu():

    pygame.init()

    const.tela

    #DEFININDO A FONTE USADA PARA EXIBIR AS OPÇÕES
    fonteOpcao = pygame.font.SysFont(const.fonte, 25, True)
    
    #CARREGANDO A IMAGEM DA SETA E REDIMENSIONANDO SEU TAMANHO
    img_seta1 = pygame.image.load(const.img_seta_direita)
    img_seta1 = pygame.transform.scale(img_seta1, (64, 64))
     
    x_seta1 = 330
    y_seta1 = 150
    
    img_seta2 = pygame.image.load(const.img_seta_esquerda)
    img_seta2 = pygame.transform.scale(img_seta2, (64, 64))

    x_seta2 = 726
    y_seta2 = 150

    autoria = fonteOpcao.render("© Created by Canceladx", True, const.cor_preta)
    opc1 = fonteOpcao.render("Multiplayer local", True, const.cor_branca)
    opc2 = fonteOpcao.render("Multiplayer online", True, const.cor_branca)
    opc3 = fonteOpcao.render("Treinamento", True, const.cor_branca)
    opc4 = fonteOpcao.render("Regras", True, const.cor_branca)
    opc5 = fonteOpcao.render("Sair", True, const.cor_branca)

    som_menu = pygame.mixer.music.load('sons/som_menu.ogg')
    som_seta = pygame.mixer.Sound('sons/som_seta.ogg')

    #pygame.mixer.music.play()

    while True:
        const.relogio.tick(const.fps)
 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
        const.tela.fill(const.plano_de_fundo_menu)
        
        pygame.draw.rect(const.tela, const.cor_opcao, (410, 140, 300, 80),0,30)
        pygame.draw.rect(const.tela, const.cor_opcao, (410, 240, 300, 80),0,30)
        pygame.draw.rect(const.tela, const.cor_opcao, (410, 340, 300, 80),0,30)
        pygame.draw.rect(const.tela, const.cor_opcao, (410, 440, 300, 80),0,30)
        pygame.draw.rect(const.tela, const.cor_opcao, (410, 540, 300, 80),0,30)
           
        const.tela.blit(opc1, (463, 168))
        const.tela.blit(opc2, (458, 268))
        const.tela.blit(opc3, (490, 368))
        const.tela.blit(opc4, (520, 468))
        const.tela.blit(opc5, (540, 568))
        const.tela.blit(autoria, (30, 600))

        #CONTROLANDO AS SETAS DO MENU
        tecla = pygame.key.get_pressed()
        
        if tecla[K_UP]:
            y_seta1 = S_praCima(y_seta1, 150)
            y_seta2 = S_praCima(y_seta2, 150)
            sleep(0.1)
            som_seta.play()

        if tecla[K_DOWN]:
            y_seta1 = S_praBaixo(y_seta1, 550)
            y_seta2 = S_praBaixo(y_seta2, 550)
            sleep(0.1)
            som_seta.play()

        #PARA A MÚSICA QUE TOCA NO MENU QUANDO ALGUMA OPÇÃO É SELECIONADA
        if tecla[K_RETURN]:
            pygame.mixer.music.stop()

        #CHAMANDO A TELA SELECIONADA COM BASE NA POSIÇÃO DA SETA
        if y_seta1 == 150 and tecla[K_RETURN]:
            tela_multijogador.exibir_tela_multijogador()

        if y_seta1 == 250 and tecla[K_RETURN]:
            tela_online.exibir_tela_online()

        if y_seta1 == 350 and tecla[K_RETURN]:
            tela_treinamento.exibir_tela_treinamento()

        if y_seta1 == 450 and tecla[K_RETURN]:
            tela_regras.exibir_tela_regras()

        if y_seta1 == 550 and tecla[K_RETURN]:
            pygame.quit()
            exit()

        const.tela.blit(img_seta1, (x_seta1, y_seta1))
        const.tela.blit(img_seta2, (x_seta2, y_seta2))

        pygame.display.flip()

        if tecla[K_ESCAPE]:
            pygame.mixer.music.stop()
        if tecla[K_TAB]:
            pygame.mixer.music.play()
