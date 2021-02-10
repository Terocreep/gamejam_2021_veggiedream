from src.Player import Player
from src.Platform import Platform
import pygame
import json

player = Player("")


class Platformer:
    def __init__(self, level):
        # self.background = pygame.image.load('images/background.png')
        player.velocity[1] = 500
        player.update([])
        player.velocity[1] = 0
        self.platforms = []

        with open("levels/lvl{}.json".format(level), 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.height = map_data['height']*64
        self.width = map_data['width']*64

        for item in map_data['blocks']:
            x, y = item[1] * 64, item[0] * 64
            mort = item[2] == 3
            trav = item[2] == 2

            # if item[2] == 1:
            self.platforms.append(Platform(x, y, map_data['block_sprite']["{}".format(item[3])].format("sol"), trav, mort))

    def update(self, x, y, screen):
        # screen.blit(self.background, pygame.Surface((1024,768)).get_rect())  "user/{}.txt".format(a)

        player.velocity[0] = 6 * x

        police = pygame.font.Font(None, 20)

        off_x = (player.rect.centerx - 1024 / 2)
        if player.rect.centerx < 1024 / 2:
            off_x = 0
        elif player.rect.centerx > self.width - 1024 / 2:
            off_x = self.width - 1024

        off_y = (player.rect.centery - 786 / 2)
        if self.height - player.rect.centery < 768 / 2:
            off_y = self.height - 768
        elif self.height - player.rect.centery > self.height - 768 / 2:
            off_y = 0

        if y == -1:
            player.jump(self.platforms)
            player.update(self.platforms)
        elif y == 1:
            player.sneak(self.platforms)
        else:
            player.update(self.platforms)
        for p in self.platforms:
            r = pygame.rect.Rect(0, 0, p.rect.w, p.rect.h)
            r.centerx = p.rect.centerx - off_x
            r.centery = p.rect.centery - off_y
            screen.blit(p.sprite, r)

        pr = pygame.rect.Rect(0, 0, player.rect.w, player.rect.h)
        pr.centerx = player.rect.centerx - off_x
        pr.centery = player.rect.centery - off_y
        screen.blit(player.sprite, pr)
