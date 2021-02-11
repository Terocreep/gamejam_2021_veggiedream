from src.Score import Score
from src.Player import Player
from src.Platform import Platform
from src.Enemy import Enemy
from src.Enemy import Lanceur
from src.Deplacement import Deplacement
from src.Covec import CoVec

from src.Player import Player
from src.Platform import Platform
import pygame
import json


class Platformer:
    def __init__(self):
        self.player = Player("", 70, 9200)

        self.height = 0
        self.width = 0

        self.score = Score("michel")
        self.score.newVar("meurt", -10)

        self.enemys = []
        self.enemys.append(
            Lanceur(Deplacement(CoVec(200, 23*64-32), CoVec(500, 23*64-32), CoVec(2, 0)), "tomate_ennemy.png", 32, 32,
                    "tomate_ennemy.png", 32, 32, 200, 40))

        self.platforms = []

    def load_level(self, level):
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
        self.player.velocity[0] = 6 * x

        if not self.player.die(self.platforms, self.enemys, self.enemys):
            off_x = (self.player.rect.centerx - 1024 / 2)
            if self.player.rect.centerx < 1024 / 2:
                off_x = 0
            elif self.player.rect.centerx > self.width - 1024 / 2:
                off_x = self.width - 1024

            off_y = (self.player.rect.centery - 786 / 2)
            if self.height - self.player.rect.centery < 768 / 2:
                off_y = self.height - 768
            elif self.height - self.player.rect.centery > self.height - 768 / 2:
                off_y = 0

            if y == -1:
                self.player.jump(31, self.platforms)
                self.player.update(self.platforms)
            elif y == 1:
                self.player.sneak(self.platforms)
            else:
                self.player.update(self.platforms)
            for p in self.platforms:
                r = pygame.rect.Rect(0, 0, p.rect.w, p.rect.h)
                r.centerx = p.rect.centerx - off_x
                r.centery = p.rect.centery - off_y
                screen.blit(p.sprite, r)

            for e in self.enemys:
                e.deplacementNormale(self.enemys)
                er = pygame.rect.Rect(0, 0, e.rect.w, e.rect.h)
                er.centerx = e.rect.centerx - off_x
                er.centery = e.rect.centery - off_y
                screen.blit(e.sprite, er)

            pr = pygame.rect.Rect(0, 0, self.player.rect.w, self.player.rect.h)
            pr.centerx = self.player.rect.centerx - off_x
            pr.centery = self.player.rect.centery - off_y
            screen.blit(self.player.sprite, pr)

        else:
            self.score.execVar("meurt")


