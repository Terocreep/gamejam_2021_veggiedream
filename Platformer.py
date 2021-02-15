from src.Score import Score
from src.Colectible import Colectible
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

        self.jump_bool = False

        self.height = 0
        self.width = 0

        self.game_over = False
        self.victory = False

        self.cadre = pygame.transform.scale(pygame.image.load("images/health_bar.png"), (402, 66))

        self.score = Score("")

        self.colectibles = []

        self.enemys = []

        # enemy template

       # self.enemys.append(Enemy(Deplacement(CoVec(44 * 64, 133 * 64 - 32), CoVec(47 * 64, 133 * 64 - 32), CoVec(2, 0)),
       #                          "tomate_ennemy.png", 32, 32))
       # self.enemys.append(Enemy(Deplacement(CoVec(64 * 64, 130 * 64 - 32), CoVec(67 * 64, 130 * 64 - 32), CoVec(2, 0)),
       #                          "tomate_ennemy.png", 32, 32))
       # self.enemys.append(
       #     Lanceur(Deplacement(CoVec(56 * 64, 120 * 64 - 32), CoVec(58 * 64, 120 * 64 - 32), CoVec(1, 0)),
       #             "tomate_ennemy.png", 32, 32,
       #             "tomate/tomate_project_2.png", 16, 16, 2 * 64, 50))

       # self.enemys.append(
       #     Lanceur(Deplacement(CoVec(86 * 64, 115 * 64 - 32), CoVec(86 * 64, 115 * 64 - 32), CoVec(0, 0)),
       #             "tomate_ennemy.png", 32, 32,
       #             "tomate/tomate_project_2.png", 16, 16, 5 * 64, 70))

        self.platforms = []

    def set_player(self, username):
        self.score= Score(username)
        self.score.newVar("meurt", -10)
        self.score.newVar("carotte", 3)
        self.score.newVar("superCarotte", 10)


    def load_level(self, level):
        with open("levels/lvl{}.json".format(level), 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.height = map_data['height']*64
        self.width = map_data['width']*64

        for item in map_data['enemys']:
            size = map_data["enemySize"][str(item[8])]
            x, y = item[0] * 64, item[1] * 64 - size
            xx, yy = item[2] * 64, item[3] * 64 - size
            vx, vy = item[4], item[5]
            type = str(item[6])

            if map_data["enemyType"][type] == "normale":
                self.enemys.append(
                    Enemy(Deplacement(CoVec(x, y), CoVec(xx, yy), CoVec(vx, vy)), map_data["enemyStyle"][str(item[7])],
                          size, size))

            elif map_data["enemyType"][type] == "lanceur":
                self.enemys.append(
                    Lanceur(Deplacement(CoVec(x, y), CoVec(xx, yy), CoVec(vx, vy)),
                            map_data["enemyStyle"][str(item[7])], size, size,
                            map_data["enemyStyle"][str(item[9])], map_data["enemySize"][str(item[10])],
                            map_data["enemySize"][str(item[10])], item[11] * 64, item[12]))

        for item in map_data['colectibls']:
            self.colectibles.append(
                Colectible(CoVec(item[0] * 64, item[1] * 64),
                           map_data["colectiblStyle"][str(item[2])],
                           int(map_data["colectiblSize"][str(item[3])]),
                           int(map_data["colectiblSize"][str(item[3])]),
                           map_data["name"][str(item[4])]))

        for item in map_data['blocks']:
            x, y = item[1] * 64, item[0] * 64
            mort = item[2] == 3
            trav = item[2] == 2

            # if item[2] == 1:
            self.platforms.append(Platform(x, y, map_data['block_sprite']["{}".format(item[3])].format("sol"), trav, mort))

    def update(self, x, y, screen):
        self.player.velocity[0] = 6 * x

        if self.player.asLaSuperCarotte:
            self.score.finPartie()
            self.victory = True
            print("mettre le code game gagner")

        else:
            if not self.player.die(self.platforms, self.enemys, self.enemys):
                self.player.collect(self.colectibles, self.score)
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
                    self.player.jump(31, self.platforms, self.jump_bool)
                    self.jump_bool = False
                    self.player.update(self.platforms)
                elif y == 1:
                    self.player.sneak(self.platforms)
                else:
                    self.player.update(self.platforms)
                    self.jump_bool = True

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

                for c in self.colectibles:
                    cr = pygame.rect.Rect(0, 0, c.rect.w, c.rect.h)
                    cr.centerx = c.rect.centerx - off_x
                    cr.centery = c.rect.centery - off_y
                    screen.blit(c.sprite, cr)

                pr = pygame.rect.Rect(0, 0, self.player.rect.w, self.player.rect.h)
                pr.centerx = self.player.rect.centerx - off_x
                pr.centery = self.player.rect.centery - off_y
                screen.blit(self.player.sprite, pr)

                screen.blit(self.cadre, (0, 0))
                self.player.update_health_bar(screen)

            else:
                self.score.execVar("meurt")
                self.player.removeHealth(20)
                if self.player.health <= 0:
                    print("metre le code game over")
                    self.score.finPartie()
                    self.game_over = True
