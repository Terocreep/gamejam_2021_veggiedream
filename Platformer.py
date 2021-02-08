from src.Player import Player
from src.Platform import Platform
import pygame


player = Player("")


class Platformer:
    def __init__(self, level):
        # self.background = pygame.image.load('images/background.png')
        player.velocity[1] = 500
        player.update([])
        player.velocity[1] = 0

        self.platforms = []
        self.platforms.append(Platform(0, 700))
        self.platforms.append(Platform(60, 700))
        self.platforms.append(Platform(120, 700))
        self.platforms.append(Platform(220, 700))
        self.platforms.append(Platform(280, 700))
        self.platforms.append(Platform(340, 700))
        self.platforms.append(Platform(440, 700))

    def update(self, x, y, screen):
        # screen.blit(self.background, pygame.Surface((1024,768)).get_rect())
        player.velocity[0] = 200 * 0.05 * x
        if y == -1:
            player.jump(self.platforms)
        player.update(self.platforms)
        for p in self.platforms:
            screen.blit(p.sprite, (p.x-2, p.y, p.x+34, p.y+32))
        screen.blit(player.sprite, player.rect)
