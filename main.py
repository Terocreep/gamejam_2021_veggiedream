import pygame
import random
from Runner import Runner
from Platformer import Platformer
from Menu import Menu
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("VeggieDream")
clock = pygame.time.Clock()
FPS = 30

#Menu
menu = Menu()

escape = False

x = 0
y = 0

phase = ""

clicking = False


def menu_update(px, py, click):
    if phase == "menu":
        menu.update(px, py, screen, click, escape)


def update(ux, uy):
    if phase == "platform":
        menu.plat.update(ux, uy, screen)
    elif phase == "runner":
        menu.run.update(ux, uy, screen)


running = True
while running:
    time = clock.tick(FPS) / 1000
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y = -1
            elif event.key == pygame.K_DOWN:
                y = 1
            elif event.key == pygame.K_LEFT:
                x = -1
            elif event.key == pygame.K_RIGHT:
                x = 1
            elif event.key == pygame.K_ESCAPE:
                escape = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x = 0
            elif event.key == pygame.K_ESCAPE:
                escape = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    mx, my = pygame.mouse.get_pos()
    menu_update(mx, my, clicking)
    if menu.run.game_over or menu.plat.game_over:
        phase = "menu"
        menu_update(mx, my, clicking)
    if menu.plat.victory:
        phase = "menu"
        menu_update(mx, my, clicking)

    if escape and phase == "":
        phase = "menu"

    if menu.platformer:
        phase = "platform"
    elif menu.runner:
        phase = "runner"

    update(x, y)

    pygame.display.update()
