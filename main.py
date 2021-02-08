import pygame
from Runner import Runner
from Platformer import Platformer
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((1024, 768))

clock = pygame.time.Clock()
FPS = 30

run = Runner(screen)
plat = Platformer(screen)

phase = "main_menu"


def update(ux, uy):
    if phase == "platform":
        plat.update(ux, uy)
    elif phase == "runner":
        run.update(ux, uy)


running = True
while running:
    time = clock.tick(FPS) / 1000
    x = 0
    y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                print("up")
                y = 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                print("right")
                y = 1
            elif event.key == pygame.K_q or event.key == pygame.K_LEFT:
                print("left")
                x = 1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print("down")
                x = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z or event.key == pygame.K_UP \
                    or event.key == pygame.K_s or event.key == pygame.K_DOWN:
                print("ud")
                y = 0
            elif event.key == pygame.K_q or event.key == pygame.K_LEFT \
                    or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print("lr")
                x = 0
    update(x, y)
    pygame.display.update()
