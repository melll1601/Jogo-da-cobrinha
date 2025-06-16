import pygame
import sys
import random

pygame.init()

som_comer = pygame.mixer.Sound("comendo.wav")
som_morrer = pygame.mixer.Sound("morre.mp3")
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.set_volume(500.00)
pygame.mixer.music.play(-1)

LARGURA, ALTURA = 600, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(" Cobrinha :D")

PRETO = (0, 0, 0)
VERDE_CLARO = (0, 255, 100)
VERDE_ESCURO = (0, 150, 50)
VERMELHO = (255, 60, 60)
CINZA_ESCURO = (30, 30, 40)
BRANCO = (255, 255, 255)
AZUL_ESCURO = (10, 10, 50)
AZUL_CLARO = (30, 60, 100)
AMARELO = (255, 230, 0)
CINZA_BOTAO = (100, 100, 100)

ROSA_CLARO = (255, 182, 193)
ROSA_MEDIO = (255, 105, 180)
ROSA_ESCURO = (219, 112, 147)

fonte = pygame.font.SysFont("consolas", 30, bold=True)
fonte_grande = pygame.font.SysFont("consolas", 50, bold=True)
fonte_pequena = pygame.font.SysFont("consolas", 24)

clock = pygame.time.Clock()
FPS = 15
TAMANHO_BLOCO = 20
TAMANHO_CABECA = 20
imagem_cabeca = pygame.image.load("cobraa.png")
imagem_cabeca = pygame.transform.scale(imagem_cabeca, (TAMANHO_CABECA, TAMANHO_CABECA))

imagem_fundo = pygame.image.load("imagem.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

def desenhar_fundo():
    TELA.blit(imagem_fundo, (0, 0))

def desenha_cobra(cobra):
    for i, bloco in enumerate(cobra):
        if i == 0:
            TELA.blit(imagem_cabeca, (bloco[0], bloco[1]))  # cabeça com imagem
        else:
            pygame.draw.rect(
                TELA, ROSA_CLARO, 
                pygame.Rect(bloco[0], bloco[1], TAMANHO_BLOCO, TAMANHO_BLOCO), 
                border_radius=6
            )

def nova_fruta():
    return [
        random.randrange(0, LARGURA, TAMANHO_BLOCO),
        random.randrange(0, ALTURA, TAMANHO_BLOCO)
    ]

def desenhar_texto(texto, cor, y, sombra=True):
    if sombra:
        sombra_txt = fonte.render(texto, True, PRETO)
        sombra_rect = sombra_txt.get_rect(center=(LARGURA // 2 + 2, y + 2))
        TELA.blit(sombra_txt, sombra_rect)
    txt = fonte.render(texto, True, cor)
    rect = txt.get_rect(center=(LARGURA // 2, y))
    TELA.blit(txt, rect)

def botao(texto, x, y, largura, altura, cor, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    botao_rect = pygame.Rect(x, y, largura, altura)

    if botao_rect.collidepoint(mouse):
        pygame.draw.rect(TELA, cor, botao_rect, border_radius=10)
        if clique[0] and acao:
            pygame.time.delay(200)
            acao()
    else:
        pygame.draw.rect(TELA, CINZA_BOTAO, botao_rect, border_radius=10)

    txt = fonte_pequena.render(texto, True, PRETO)
    txt_rect = txt.get_rect(center=(x + largura // 2, y + altura // 2))
    TELA.blit(txt, txt_rect)

def mostrar_ajuda():
    ajuda_ativa = True
    etapa = 0  # Etapas do tutorial
    mensagens = [
        "Use as setas para mover",
        "Coma a fruta para crescer",
        "Evite bater nas paredes",
        "Evite colidir com o próprio corpo",
        "Boa sorte! :)",
        "Clique para voltar ao menu"
    ]

    while ajuda_ativa:
        desenhar_fundo()
        desenhar_texto("Tutorial", AMARELO, 100)

        # Mostrar mensagem da etapa atual
        if etapa < len(mensagens):
            desenhar_texto(mensagens[etapa], BRANCO, 220)
        else:
            ajuda_ativa = False
            break

        desenhar_texto("Clique para continuar", ROSA_MEDIO, 500)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                etapa += 1
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ajuda_ativa = False

def game_over(pontuacao):
    while True:
        desenhar_fundo()
        desenhar_texto(" GAME OVER =(", VERMELHO, ALTURA // 2 - 40)
        desenhar_texto(f"Pontuação: {pontuacao}", BRANCO, ALTURA // 2)
        desenhar_texto("Clique para voltar ao MENU", BRANCO, ALTURA // 2 + 40)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return  # Também volta para o jogo

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return

def jogar():
    cobra = [[100, 100]]
    direcao = (TAMANHO_BLOCO, 0)
    fruta = nova_fruta()
    pontuacao = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao[1] == 0:
                    direcao = (0, -TAMANHO_BLOCO)
                if evento.key == pygame.K_DOWN and direcao[1] == 0:
                    direcao = (0, TAMANHO_BLOCO)
                if evento.key == pygame.K_LEFT and direcao[0] == 0:
                    direcao = (-TAMANHO_BLOCO, 0)
                if evento.key == pygame.K_RIGHT and direcao[0] == 0:
                    direcao = (TAMANHO_BLOCO, 0)

        nova_cabeca = [cobra[0][0] + direcao[0], cobra[0][1] + direcao[1]]
        cobra.insert(0, nova_cabeca)

        if cobra[0] == fruta:
            fruta = nova_fruta()
            pontuacao += 1
            som_comer.play()

        else:
            cobra.pop()

        if (
            cobra[0][0] < 0 or cobra[0][0] >= LARGURA or
            cobra[0][1] < 0 or cobra[0][1] >= ALTURA or
            cobra[0] in cobra[1:]
        ):
            som_morrer.play()
            break

        desenhar_fundo()
        desenha_cobra(cobra)
        pygame.draw.rect(TELA, VERMELHO, pygame.Rect(fruta[0], fruta[1], TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=4)
        desenhar_texto(f"Pontuação: {pontuacao}", BRANCO, 30, sombra=False)
        pygame.display.update()
        clock.tick(FPS)

    game_over(pontuacao)

def tela_inicial():
    while True:
        desenhar_fundo()
        desenhar_texto("Cobrinha ⚆_⚆", ROSA_MEDIO, 100)
        botao("Jogar", 200, 220, 200, 50, ROSA_CLARO, jogar)
        botao("Ajuda", 200, 290, 200, 50, ROSA_MEDIO, mostrar_ajuda)
        botao("Sair", 200, 360, 200, 50, ROSA_ESCURO, pygame.quit)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

tela_inicial()