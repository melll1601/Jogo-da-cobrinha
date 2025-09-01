import pygame
import sys
import random
import math

# Inicialização do pygame e sons
pygame.init()
som_comer = pygame.mixer.Sound("comendo.wav")
som_morrer = pygame.mixer.Sound("morre.mp3")
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Parâmetros da tela
LARGURA, ALTURA = 600, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha :D")

# Cores usadas no jogo
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

# Fontes
fonte = pygame.font.SysFont("consolas", 30, bold=True)
fonte_grande = pygame.font.SysFont("consolas", 50, bold=True)
fonte_pequena = pygame.font.SysFont("consolas", 20)

clock = pygame.time.Clock()
FPS = 15
TAMANHO_BLOCO = 20
TAMANHO_CABECA = 20
imagem_cabeca = pygame.image.load("cobraa.png")
imagem_cabeca = pygame.transform.scale(imagem_cabeca, (TAMANHO_CABECA, TAMANHO_CABECA))

imagem_fundo = pygame.image.load("imagem.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

mensagem_tempo = 0
mensagem_texto = ""

# Inimigo
inimigo_pos = [random.randint(0, LARGURA - TAMANHO_BLOCO), random.randint(0, ALTURA - TAMANHO_BLOCO)]
inimigo_vel = [random.choice([-2, 2]), random.choice([-2, 2])]
inimigo_cor = AZUL_CLARO
contador_inimigo = 0

def calcular_distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def desenhar_balao(texto):
    largura_balao = 300
    altura_balao = 40
    x = 150
    y = 40
    pygame.draw.rect(TELA, BRANCO, (x, y, largura_balao, altura_balao), border_radius=12)
    pygame.draw.rect(TELA, PRETO, (x, y, largura_balao, altura_balao), 2, border_radius=12)
    txt = fonte_pequena.render(texto, True, PRETO)
    txt_rect = txt.get_rect(center=(x + largura_balao // 2, y + altura_balao // 2))
    TELA.blit(txt, txt_rect)

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

def desenhar_timer(tempo_passado):
    minutos = tempo_passado // 60000
    segundos = (tempo_passado % 60000) // 1000
    texto = f"Tempo: {minutos:02}:{segundos:02}"
    desenhar_texto(texto, BRANCO, 90, sombra=False)

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

def game_over(pontuacao):
    while True:
        desenhar_fundo()
        desenhar_texto(" GAME OVER =(", VERMELHO, ALTURA // 2 - 40)
        desenhar_texto(str(pontuacao), BRANCO, ALTURA // 2)
        desenhar_texto("Clique para voltar ao menu", BRANCO, ALTURA // 2 + 40)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                tela_inicial()
                return

def tela_ajuda():
    mensagens = [
        "Jogador 1: setas ↑ ↓ ← →",
        "Jogador 2: W A S D",
        "Evite o inimigo azul!",
        "Coma frutas para ganhar energia",
        "Colidir com jogador= Game Over"
    ]
    indice = 0

    while True:
        desenhar_fundo()
        desenhar_texto("AJUDA", AMARELO, 80)
        desenhar_texto(mensagens[indice], BRANCO, 200)
        botao("Voltar", 200, 400, 200, 50, ROSA_CLARO, tela_inicial)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                indice += 1
                if indice >= len(mensagens):
                    indice = 0  # Reinicia o ciclo


def jogar():
    global mensagem_tempo, mensagem_texto, inimigo_pos, inimigo_vel, contador_inimigo
    cobra1 = [[100, 100]]
    direcao1 = (TAMANHO_BLOCO, 0)
    cobra2 = [[400, 400]]
    direcao2 = (-TAMANHO_BLOCO, 0)
    fruta = nova_fruta()
    pontuacao1 = 0
    pontuacao2 = 0
    energia1 = 5
    energia2 = 5
    mensagem_texto = "Vamos crescer juntos!"
    mensagem_tempo = pygame.time.get_ticks()
    inicio_tempo = pygame.time.get_ticks()

    falas_comer = [
        "Ai que gostoso essa comida!",
        "Delícia de fruta!",
        "Yummy! Mais uma!",
        "Comidaaa \\o/",
        "Estou crescendo bem!"
    ]

    while True:
        tempo_passado = pygame.time.get_ticks() - inicio_tempo
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

        nova_cabeca1 = [cobra1[0][0] + direcao1[0], cobra1[0][1] + direcao1[1]]
        nova_cabeca2 = [cobra2[0][0] + direcao2[0], cobra2[0][1] + direcao2[1]]
        cobra1.insert(0, nova_cabeca1)
        cobra2.insert(0, nova_cabeca2)

        for cobra, idx in [(cobra1, 1), (cobra2, 2)]:
            if calcular_distancia(cobra[0], fruta) < TAMANHO_BLOCO:
                fruta = nova_fruta()
                som_comer.play()
                if idx == 1:
                    pontuacao1 += 1
                    energia1 += 1
                else:
                    pontuacao2 += 1
                    energia2 += 1
                mensagem_texto = random.choice(falas_comer)
                mensagem_tempo = pygame.time.get_ticks()
            else:
                cobra.pop()

        contador_inimigo += 1
        if contador_inimigo % 60 == 0:
            inimigo_vel = [random.choice([-3, -2, 2, 3]), random.choice([-3, -2, 2, 3])]
        inimigo_pos[0] += inimigo_vel[0]
        inimigo_pos[1] += inimigo_vel[1]
        if inimigo_pos[0] < 0 or inimigo_pos[0] > LARGURA - TAMANHO_BLOCO:
            inimigo_vel[0] *= -1
        if inimigo_pos[1] < 0 or inimigo_pos[1] > ALTURA - TAMANHO_BLOCO:
            inimigo_vel[1] *= -1

        def verifica_colisoes(cobra, energia):
            if (cobra[0][0] < 0 or cobra[0][0] >= LARGURA or
                cobra[0][1] < 0 or cobra[0][1] >= ALTURA or
                cobra[0] in cobra[1:] or
                calcular_distancia(cobra[0], inimigo_pos) < TAMANHO_BLOCO):
                energia -= 1
                som_morrer.play()
            return energia

        energia1 = verifica_colisoes(cobra1, energia1)
        energia2 = verifica_colisoes(cobra2, energia2)

        if cobra1[0] in cobra2 or cobra2[0] in cobra1:
            som_morrer.play()
            game_over(f"P1: {pontuacao1} | P2: {pontuacao2} | Tempo: {tempo_passado // 1000}s")
            return

        if energia1 <= 0 or energia2 <= 0:
            game_over(f"P1: {pontuacao1} | P2: {pontuacao2} | Tempo: {tempo_passado // 1000}s")
            return

        desenhar_fundo()
        desenha_cobra(cobra1)
        desenha_cobra(cobra2)
        pygame.draw.rect(TELA, VERMELHO, pygame.Rect(fruta[0], fruta[1], TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=4)
        pygame.draw.rect(TELA, inimigo_cor, pygame.Rect(inimigo_pos[0], inimigo_pos[1], TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=6)
        desenhar_texto(f"P1 Pontuação: {pontuacao1} | Energia: {energia1}", ROSA_CLARO, 30, sombra=False)
        desenhar_texto(f"P2 Pontuação: {pontuacao2} | Energia: {energia2}", ROSA_ESCURO, 60, sombra=False)
        desenhar_timer(tempo_passado)
        if pygame.time.get_ticks() - mensagem_tempo < 2000:
            desenhar_balao(mensagem_texto)
        pygame.display.update()
        clock.tick(FPS)

def tela_inicial():
    while True:
        desenhar_fundo()
        desenhar_texto("Cobrinha :D", ROSA_MEDIO, 100)
        botao("Jogar", 200, 220, 200, 50, ROSA_CLARO, jogar)
        botao("Ajuda", 200, 290, 200, 50, ROSA_MEDIO, tela_ajuda)
        botao("Sair", 200, 360, 200, 50, ROSA_ESCURO, pygame.quit)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

tela_inicial()