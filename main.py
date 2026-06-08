from src.jogo import executar_jogo


if __name__ == "__main__":
    # Ponto de entrada da aplicação.
    executar_jogo()
import pygame
import random

# Configurações
LARGURA = 800
ALTURA = 600
FPS = 60

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 150, 255)
VERMELHO = (255, 0, 0)


def criar_nave():
    return pygame.Rect(LARGURA // 2, ALTURA - 80, 50, 50)


def criar_meteoro():
    return pygame.Rect(random.randint(0, LARGURA - 40), -40, 40, 40)


def mover_nave(nave, teclas):
    velocidade = 5

    if teclas[pygame.K_a]:
        nave.x -= velocidade

    if teclas[pygame.K_d]:
        nave.x += velocidade

    if teclas[pygame.K_w]:
        nave.y -= velocidade

    if teclas[pygame.K_s]:
        nave.y += velocidade

    # Limites da tela
    nave.x = max(0, min(nave.x, LARGURA - nave.width))
    nave.y = max(0, min(nave.y, ALTURA - nave.height))


def mover_meteoro(meteoro, velocidade):
    meteoro.y += velocidade

    if meteoro.top > ALTURA:
        meteoro.x = random.randint(0, LARGURA - meteoro.width)
        meteoro.y = -50


def desenhar_tela(tela, nave, meteoro, tempo):
    tela.fill(PRETO)

    pygame.draw.rect(tela, AZUL, nave)
    pygame.draw.rect(tela, VERMELHO, meteoro)

    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render(f"Tempo: {tempo}", True, BRANCO)

    tela.blit(texto, (10, 10))

    pygame.display.flip()


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Meteor Fall")

    relogio = pygame.time.Clock()

    nave = criar_nave()
    meteoro = criar_meteoro()

    rodando = True
    game_over = False

    tempo_inicio = pygame.time.get_ticks()

    while rodando:

        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if not game_over:

            teclas = pygame.key.get_pressed()

            mover_nave(nave, teclas)

            tempo_atual = (pygame.time.get_ticks() - tempo_inicio) // 1000

            velocidade_meteoro = 5 + (tempo_atual // 10)

            mover_meteoro(meteoro, velocidade_meteoro)

            if nave.colliderect(meteoro):
                game_over = True

            desenhar_tela(tela, nave, meteoro, tempo_atual)

        else:
            tela.fill(PRETO)

            fonte = pygame.font.SysFont(None, 50)

            texto1 = fonte.render("GAME OVER", True, BRANCO)
            texto2 = fonte.render(
                f"Tempo sobrevivido: {tempo_atual}s",
                True,
                BRANCO
            )

            tela.blit(texto1, (250, 250))
            tela.blit(texto2, (180, 320))

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
