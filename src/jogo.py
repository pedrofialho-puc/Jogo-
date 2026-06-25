import pygame
import random
import os

LARGURA = 800
ALTURA = 600
FPS = 60

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 150, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

ARQUIVO_RANKING = "data/ranking.txt"


def criar_nave():
    return pygame.Rect(LARGURA // 2, ALTURA - 80, 50, 50)


def criar_meteoro():
    return pygame.Rect(
        random.randint(0, LARGURA - 40),
        random.randint(-300, -40),
        40,
        40
    )


def criar_powerup():
    x = random.randint(50, LARGURA - 100)
    y = random.randint(50, ALTURA - 200)
    return pygame.Rect(x, y, 60, 30)


def mover_nave(nave, teclas):
    velocidade = 6

    if teclas[pygame.K_a]:
        nave.x -= velocidade
    if teclas[pygame.K_d]:
        nave.x += velocidade
    if teclas[pygame.K_w]:
        nave.y -= velocidade
    if teclas[pygame.K_s]:
        nave.y += velocidade

    nave.x = max(0, min(nave.x, LARGURA - nave.width))
    nave.y = max(0, min(nave.y, ALTURA - nave.height))


def mover_meteoro(meteoro, velocidade):
    meteoro.y += velocidade

    if meteoro.top > ALTURA:
        meteoro.x = random.randint(0, LARGURA - meteoro.width)
        meteoro.y = random.randint(-300, -40)


def carregar_recorde():
    if not os.path.exists(ARQUIVO_RANKING):
        return 0

    try:
        with open(ARQUIVO_RANKING, "r") as arquivo:
            pontuacoes = []

            for linha in arquivo:
                linha = linha.strip()
                if linha.isdigit():
                    pontuacoes.append(int(linha))

            if pontuacoes:
                return max(pontuacoes)
    except:
        pass

    return 0


def salvar_pontuacao(pontos):
    os.makedirs("data", exist_ok=True)
    with open(ARQUIVO_RANKING, "a") as arquivo:
        arquivo.write(f"{pontos}\n")


def desenhar_botao(tela, texto, x, y, largura, altura):
    mouse = pygame.mouse.get_pos()
    botao = pygame.Rect(x, y, largura, altura)

    cor = (100, 100, 100)
    if botao.collidepoint(mouse):
        cor = (180, 180, 180)

    pygame.draw.rect(tela, cor, botao)

    fonte = pygame.font.SysFont(None, 40)
    txt = fonte.render(texto, True, BRANCO)

    tela.blit(
        txt,
        (
            x + largura // 2 - txt.get_width() // 2,
            y + altura // 2 - txt.get_height() // 2
        )
    )

    return botao

def desenhar_tela(
    tela,
    nave,
    meteoros,
    powerup,
    pontos,
    recorde,
    nave_img,
    meteoro_img,
    vidas,
    tempo
):
    tela.fill(PRETO)

    tela.blit(nave_img, nave)

    for meteoro in meteoros:
        tela.blit(meteoro_img, meteoro)
    fonte_power = pygame.font.SysFont(None, 32)
    texto_power = fonte_power.render("trair", True, VERDE)
    tela.blit(texto_power, (powerup.x, powerup.y))
    fonte = pygame.font.SysFont(None, 36)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, BRANCO)
    texto_vidas = fonte.render(f"Vida: {vidas}", True, BRANCO)
    texto_tempo = fonte.render(f"Tempo: {tempo}s", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_recorde, (10, 50))
    tela.blit(texto_vidas, (10, 90))
    tela.blit(texto_tempo, (10, 130))
    pygame.display.flip()
def main():

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Meteor Fall")

    nave_img = pygame.image.load("assets/heitor.jpeg")
    nave_img = pygame.transform.scale(nave_img, (50, 50))

    meteoro_img = pygame.image.load("assets/ex.jpeg")
    meteoro_img = pygame.transform.scale(meteoro_img, (40, 40))

    relogio = pygame.time.Clock()


    tela_inicio = True
    while tela_inicio:
        tela.fill(PRETO)

        titulo = pygame.font.SysFont(None, 80)
        texto = titulo.render("METEOR FALL", True, BRANCO)
        tela.blit(texto, (190, 150))

        botao_jogar = desenhar_botao(tela, "JOGAR", 300, 300, 200, 70)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    tela_inicio = False

    nave = criar_nave()
    meteoros = [criar_meteoro() for _ in range(5)]
    powerup = criar_powerup()

    rodando = True
    game_over = False

    vidas = 1

    powerup_ativo = False
    tempo_powerup = 0

    tempo_inicio = pygame.time.get_ticks()
    recorde = carregar_recorde()
    pontuacao_salva = False

    while rodando:

        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if game_over and evento.type == pygame.MOUSEBUTTONDOWN:
                botao_reiniciar = desenhar_botao(
                    tela, "JOGAR NOVAMENTE", 220, 420, 350, 70
                )

                if botao_reiniciar.collidepoint(evento.pos):
                    main()
                    return

        if not game_over:

            teclas = pygame.key.get_pressed()
            mover_nave(nave, teclas)

            tempo_atual = (pygame.time.get_ticks() - tempo_inicio) // 1000
            pontos = tempo_atual * 10

            velocidade_meteoro = 5 + (tempo_atual // 10)

            if powerup_ativo:
                velocidade_meteoro = max(2, velocidade_meteoro - 3)

                if pygame.time.get_ticks() - tempo_powerup > 5000:
                    powerup_ativo = False

            for meteoro in meteoros:
                mover_meteoro(meteoro, velocidade_meteoro)

                if nave.colliderect(meteoro):
                    vidas -= 1
                    if vidas <= 0:
                        game_over = True

            if nave.colliderect(powerup):
                powerup_ativo = True
                tempo_powerup = pygame.time.get_ticks()
                powerup = criar_powerup()

            desenhar_tela(
                tela,
                nave,
                meteoros,
                powerup,
                pontos,
                recorde,
                nave_img,
                meteoro_img,
                vidas,
                tempo_atual
            )

        else:

            if not pontuacao_salva:
                salvar_pontuacao(pontos)

                if pontos > recorde:
                    recorde = pontos

                pontuacao_salva = True

            tela.fill(PRETO)

            fonte = pygame.font.SysFont(None, 50)

            texto1 = fonte.render("GAME OVER", True, BRANCO)
            texto2 = fonte.render(f"Pontuacao: {pontos}", True, BRANCO)
            texto3 = fonte.render(f"Recorde: {recorde}", True, BRANCO)

            tela.blit(texto1, (250, 200))
            tela.blit(texto2, (220, 280))
            tela.blit(texto3, (220, 340))

            desenhar_botao(tela, "JOGAR NOVAMENTE", 220, 420, 350, 70)

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
