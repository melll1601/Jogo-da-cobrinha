import pygame
import sys
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Sons e música
som_comer = pygame.mixer.Sound("comendo.wav")
som_morrer = pygame.mixer.Sound("morre.mp3")
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Tela
LARGURA, ALTURA = 600, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha :D")

# Cores
PRETO = (0, 0, 0)
VERMELHO = (255, 60, 60)
BRANCO = (255, 255, 255)
AMARELO = (255, 230, 0)
CINZA_BOTAO = (100, 100, 100)
ROSA_CLARO = (255, 182, 193)
ROSA_MEDIO = (255, 105, 180)
ROSA_ESCURO = (219, 112, 147)

# Fontes
fonte = pygame.font.SysFont("consolas", 30, bold=True)
fonte_grande = pygame.font.SysFont("consolas", 50, bold=True)
fonte_pequena = pygame.font.SysFont("consolas", 24)

# Imagens
TAMANHO_BLOCO = 20
TAMANHO_CABECA = 20
imagem_cabeca = pygame.image.load("cobraa.png")
imagem_cabeca = pygame.transform.scale(imagem_cabeca, (TAMANHO_CABECA, TAMANHO_CABECA))
imagem_fundo = pygame.image.load("imagem.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

clock = pygame.time.Clock()
FPS = 15

# Funções
def desenhar_fundo():
    TELA.blit(imagem_fundo, (0, 0))

def desenha_cobra(cobra):
    for i, bloco in enumerate(cobra):
        if i == 0:
            TELA.blit(imagem_cabeca, (bloco[0], bloco[1]))
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
    etapa = 0
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

def game_over_pvp(p1, p2, tempo, vencedor):
    while True:
        desenhar_fundo()
        desenhar_texto("GAME OVER", VERMELHO, 150)
        desenhar_texto(f"Pontuação P1: {p1} | P2: {p2}", BRANCO, 220)
        desenhar_texto(f"Tempo total: {tempo} segundos", BRANCO, 260)
        desenhar_texto(vencedor, AMARELO, 310)
        desenhar_texto("Clique para voltar ao MENU", BRANCO, 400)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return

def jogar():
    tempo_inicio = pygame.time.get_ticks()
    cobra1 = [[100, 100]]
    direcao1 = (TAMANHO_BLOCO, 0)
    cobra2 = [[400, 400]]
    direcao2 = (-TAMANHO_BLOCO, 0)

    fruta = nova_fruta()
    pontuacao1 = 0
    pontuacao2 = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao1[1] == 0:
                    direcao1 = (0, -TAMANHO_BLOCO)
                if evento.key == pygame.K_DOWN and direcao1[1] == 0:
                    direcao1 = (0, TAMANHO_BLOCO)
                if evento.key == pygame.K_LEFT and direcao1[0] == 0:
                    direcao1 = (-TAMANHO_BLOCO, 0)
                if evento.key == pygame.K_RIGHT and direcao1[0] == 0:
                    direcao1 = (TAMANHO_BLOCO, 0)

                if evento.key == pygame.K_w and direcao2[1] == 0:
                    direcao2 = (0, -TAMANHO_BLOCO)
                if evento.key == pygame.K_s and direcao2[1] == 0:
                    direcao2 = (0, TAMANHO_BLOCO)
                if evento.key == pygame.K_a and direcao2[0] == 0:
                    direcao2 = (-TAMANHO_BLOCO, 0)
                if evento.key == pygame.K_d and direcao2[0] == 0:
                    direcao2 = (TAMANHO_BLOCO, 0)

        # Atualiza a posição
        nova_cabeca1 = [cobra1[0][0] + direcao1[0], cobra1[0][1] + direcao1[1]]
        nova_cabeca2 = [cobra2[0][0] + direcao2[0], cobra2[0][1] + direcao2[1]]
        cobra1.insert(0, nova_cabeca1)
        cobra2.insert(0, nova_cabeca2)

        # Comer fruta
        if cobra1[0] == fruta:
            fruta = nova_fruta()
            pontuacao1 += 1
            som_comer.play()
        else:
            cobra1.pop()

        if cobra2[0] == fruta:
            fruta = nova_fruta()
            pontuacao2 += 1
            som_comer.play()
        else:
            cobra2.pop()

        # Colisões
        perdeu1 = (
            cobra1[0][0] < 0 or cobra1[0][0] >= LARGURA or
            cobra1[0][1] < 0 or cobra1[0][1] >= ALTURA or
            cobra1[0] in cobra1[1:] or
            cobra1[0] in cobra2
        )
        perdeu2 = (
            cobra2[0][0] < 0 or cobra2[0][0] >= LARGURA or
            cobra2[0][1] < 0 or cobra2[0][1] >= ALTURA or
            cobra2[0] in cobra2[1:] or
            cobra2[0] in cobra1
        )

        if perdeu1 or perdeu2 or cobra1[0] == cobra2[0]:
            som_morrer.play()
            tempo_final = (pygame.time.get_ticks() - tempo_inicio) // 1000
            if perdeu1 and not perdeu2:
                vencedor = "Jogador 2 venceu!"
            elif perdeu2 and not perdeu1:
                vencedor = "Jogador 1 venceu!"
            elif cobra1[0] == cobra2[0] or (perdeu1 and perdeu2):
                vencedor = "Empate!"
            else:
                vencedor = "Fim de jogo!"

            game_over_pvp(pontuacao1, pontuacao2, tempo_final, vencedor)
            return

        # Desenhar
        desenhar_fundo()
        desenha_cobra(cobra1)
        desenha_cobra(cobra2)
        pygame.draw.rect(TELA, VERMELHO, pygame.Rect(fruta[0], fruta[1], TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=4)
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
        desenhar_texto(f"P1: {pontuacao1}  P2: {pontuacao2}  Tempo: {tempo_decorrido}s", BRANCO, 30, sombra=False)
        pygame.display.update()
        clock.tick(FPS)

def sair():
    pygame.quit()
    sys.exit()

def tela_inicial():
    while True:
        desenhar_fundo()
        desenhar_texto("Cobrinha ⚆_⚆", ROSA_MEDIO, 100)
        botao("Jogar", 200, 220, 200, 50, ROSA_CLARO, jogar)
        botao("Ajuda", 200, 290, 200, 50, ROSA_MEDIO, mostrar_ajuda)
        botao("Sair", 200, 360, 200, 50, ROSA_ESCURO, sair)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair()

# Iniciar o jogo
tela_inicial()
