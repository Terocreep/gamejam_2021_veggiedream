import pygame
import math

from Platformer import Platformer
from Runner import Runner


class Menu:

    def __init__(self):
        self.nbbg = 0

        self.anim_1 = True
        self.anim_2 = False
        self.anim_3 = False

        self.alpha = 0

        self.rabbitx = -64
        self.rabbity = 700
        self.move = 0

        self.run = Runner()
        self.plat = Platformer()

        self.font_letter = pygame.font.Font("font/Daydream.ttf", 20)
        self.font_name = pygame.font.Font("font/Daydream.ttf", 50)

        self.background = pygame.transform.scale(pygame.image.load("images/menu_images/background.png"), (1024, 768))

        self.lapin_marche = [
            pygame.transform.scale(pygame.image.load("images/lapin_d_1.png"), (135, 135)),
            pygame.transform.scale(pygame.image.load("images/lapin_d_2.png"), (135, 135)),
            pygame.transform.scale(pygame.image.load("images/lapin_d_3.png"), (135, 135)),
            pygame.transform.scale(pygame.image.load("images/lapin_d_4.png"), (135, 135))
        ]
        self.lapin_dodo = [
            pygame.transform.flip(pygame.image.load("images/menu_images/lapin_dodo_1.png"), True, False),
            pygame.transform.flip(pygame.image.load("images/menu_images/lapin_dodo_2.png"), True, False),
            pygame.transform.flip(pygame.image.load("images/menu_images/lapin_dodo_3.png"), True, False),
            pygame.transform.flip(pygame.image.load("images/menu_images/lapin_dodo_4.png"), True, False)
        ]

        self.play = [pygame.image.load("images/menu_images/play_button.png"),
                     pygame.image.load("images/menu_images/play_button_2.png")]
        self.credits = [pygame.image.load("images/menu_images/credits_button.png"),
                        pygame.image.load("images/menu_images/credits_button_2.png")]
        self.arcade = [pygame.image.load("images/menu_images/arcade_button.png"),
                       pygame.image.load("images/menu_images/arcade_button_2.png")]
        self.campagne = [pygame.image.load("images/menu_images/campagne_button.png"),
                         pygame.image.load("images/menu_images/campagne_button_2.png")]
        self.title = [pygame.image.load("images/menu_images/title_white.png"),
                      pygame.image.load("images/menu_images/title_black.png")]
        self.delet = [pygame.image.load("images/menu_images/suppr_fondnoir.png"),
                      pygame.image.load("images/menu_images/suppr_fondblanc.png")]
        self.mouse = pygame.rect.Rect(0, 0, 1, 1)

        self.was_clicked = False

        self.play_hover = False
        self.credits_hover = False

        self.play_bool = False
        self.credits_bool = False

        self.select_level = False

        self.prep_runner = False
        self.prep_platformer = False

        self.runner = False
        self.platformer = False

        self.music = True
        pygame.mixer.init()
        pygame.mixer.music.load("musics/menu_simple.ogg")
        pygame.mixer.music.play(-1)

        self.name = ""

        self.char = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z", "0",
            "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]

        self.key = []
        for i in self.char:
            self.key.append((50 + 60 * (self.char.index(i) % 9),
                             768 / 2 + 50 + 60 * (math.trunc(self.char.index(i) / 9)),
                             (self.font_letter.render(i, False, (255, 255, 255)),
                              pygame.image.load("images/menu_images/cadre_noir_fondnoir.png")),
                             (self.font_letter.render(i, False, (0, 0, 0)),
                              pygame.image.load("images/menu_images/cadre_noir_fondblanc.png")),
                             i
                             ))

        self.lvl = [
            "1", "2"
        ]

        self.key_level = []
        for i in self.lvl:
            self.key_level.append((50 + 60 * (self.lvl.index(i) % 9),
                                   768 / 2 + 50 + 60 * (math.trunc(self.lvl.index(i) / 9)),
                                   (self.font_letter.render(i, False, (255, 255, 255)),
                                    pygame.image.load("images/menu_images/cadre_noir_fondnoir.png")),
                                   (self.font_letter.render(i, False, (0, 0, 0)),
                                    pygame.image.load("images/menu_images/cadre_noir_fondblanc.png")),
                                   i
                                   ))
        self.click = False

    def update(self, mx, my, screen, click):
        self.mouse.x = mx
        self.mouse.y = my
        self.nbbg += 1
        if self.nbbg >= 30:
            self.nbbg = 0

        screen.blit(self.background, pygame.Surface((1024, 768)).get_rect())

        if not self.music:
            pygame.mixer.music.stop()

        # select level
        if self.play_bool and not self.credits_bool and self.select_level \
                and not self.anim_1 and not self.anim_2 and not self.anim_3:
            # Mise en place titre
            rect_title = self.title[0].get_rect()
            rect_title.centerx = 1024 / 2
            rect_title.top = 50
            screen.blit(self.title[0], rect_title)

            nrender = self.font_name.render(self.name, False, (255, 255, 255))
            nrect = nrender.get_rect()
            nrect.centerx = 1024 / 2
            nrect.y = 190
            screen.blit(nrender, nrect)

            for k in self.key_level:
                re = pygame.rect.Rect(k[0], k[1], 50, 50)
                if re.colliderect(self.mouse):
                    screen.blit(k[3][1], re)
                    rt = k[3][0].get_rect()
                    rt.centerx = re.centerx
                    rt.centery = re.centery
                    screen.blit(k[3][0], rt)
                    if not click and self.was_clicked:
                        print("click")
                        self.plat.load_level(k[4])
                        self.prep_platformer = True
                        self.anim_3 = True
                else:
                    screen.blit(k[2][1], re)
                    rt = k[2][0].get_rect()
                    rt.centerx = re.centerx
                    rt.centery = re.centery
                    screen.blit(k[2][0], rt)

            # mise en place du lapin
            rl = self.lapin_marche[0].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            screen.blit(pygame.transform.flip(self.lapin_marche[0], True, False), rl)
        # menu play
        if self.play_bool and not self.credits_bool and not self.select_level \
                and not self.anim_1 and not self.anim_2 and not self.anim_3:
            # Mise en place titre
            rect_title = self.title[0].get_rect()
            rect_title.centerx = 1024 / 2
            rect_title.top = 50
            screen.blit(self.title[0], rect_title)

            # Mise en place campagne
            rect_campagne = self.campagne[0].get_rect()
            rect_campagne.right = 1024 / 2 - 50
            rect_campagne.top = 300
            if rect_campagne.colliderect(self.mouse):
                screen.blit(self.campagne[1], rect_campagne)
                self.play_hover = True
                if not click and self.was_clicked:
                    self.select_level = True
            else:
                screen.blit(self.campagne[0], rect_campagne)
                self.play_hover = False

            # Mise en place arcade
            rect_arcade = self.arcade[0].get_rect()
            rect_arcade.left = 1024 / 2 + 50
            rect_arcade.top = 300
            if rect_arcade.colliderect(self.mouse):
                screen.blit(self.arcade[1], rect_arcade)
                if not click and self.was_clicked:
                    self.prep_runner = True
                    self.anim_3 = True
            else:
                screen.blit(self.arcade[0], rect_arcade)
                self.credits_hover = False

            nrender = self.font_name.render(self.name, False, (255, 255, 255))
            nrect = nrender.get_rect()
            nrect.centerx = 1024 / 2
            nrect.y = 190
            screen.blit(nrender, nrect)

            for k in self.key:
                re = pygame.rect.Rect(k[0], k[1], 50, 50)
                if re.colliderect(self.mouse):
                    screen.blit(k[3][1], re)
                    rt = k[3][0].get_rect()
                    rt.centerx = re.centerx
                    rt.centery = re.centery
                    screen.blit(k[3][0], rt)
                    if not click and self.was_clicked:
                        self.name += k[4]
                else:
                    screen.blit(k[2][1], re)
                    rt = k[2][0].get_rect()
                    rt.centerx = re.centerx
                    rt.centery = re.centery
                    screen.blit(k[2][0], rt)

            # Mise en place delet
            rect_delet = self.delet[0].get_rect()
            rect_delet.left = 590
            rect_delet.top = 768 / 2 + 50
            if rect_delet.colliderect(self.mouse):
                screen.blit(self.delet[1], rect_delet)
                if not click and self.was_clicked:
                    self.name = self.name[:-1]
            else:
                screen.blit(self.delet[0], rect_delet)

            # mise en place du lapin
            rl = self.lapin_marche[0].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            screen.blit(pygame.transform.flip(self.lapin_marche[0], True, False), rl)
        # select level
        if not self.play_bool and not self.credits_bool \
                and not self.anim_1 and not self.anim_2 and not self.anim_3:

            # Mise en place titre
            rect_title = self.title[0].get_rect()
            rect_title.centerx = 1024 / 2
            rect_title.top = 50
            screen.blit(self.title[0], rect_title)

            # Mise en place play
            rect_play = self.play[0].get_rect()
            rect_play.centerx = 1024 / 2
            rect_play.top = 190
            if rect_play.colliderect(self.mouse):
                screen.blit(self.play[1], rect_play)
                self.play_hover = True
            else:
                screen.blit(self.play[0], rect_play)
                self.play_hover = False

            # Mise en place credits
            rect_credits = self.credits[0].get_rect()
            rect_credits.centerx = 1024 / 2
            rect_credits.top = 300
            if rect_credits.colliderect(self.mouse):
                screen.blit(self.credits[1], rect_credits)
                self.credits_hover = True
            else:
                screen.blit(self.credits[0], rect_credits)
                self.credits_hover = False

            # mise en place du lapin
            rl = self.lapin_marche[0].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            screen.blit(self.lapin_marche[0], rl)

            if not click and self.was_clicked and self.play_hover:
                print("play")
                self.music = False
                self.play_bool = True
                self.anim_2 = True

            if not click and self.was_clicked and self.credits_hover:
                print("credits")
                self.credits_bool = True
                self.anim_2 = True

        self.was_clicked = click

        if self.anim_1:
            rl = self.lapin_marche[math.trunc(self.nbbg / 30 * 4)].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            screen.blit(self.lapin_marche[math.trunc(self.nbbg / 30 * 4)], rl)
            self.rabbitx += 4
            if self.nbbg == 0 and self.move == 3:
                self.anim_1 = False
                self.move = 0
            elif self.nbbg == 0:
                self.move += 1

        if self.anim_2:
            rl = self.lapin_marche[math.trunc(self.nbbg / 30 * 4)].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            screen.blit(self.lapin_marche[math.trunc(self.nbbg / 30 * 4)], rl)
            self.rabbitx += 5
            if self.nbbg == 0 and self.move == 2:
                self.anim_2 = False
                self.move = 0
            elif self.nbbg == 0:
                self.move += 1

        if self.anim_3:
            rl = self.lapin_marche[0].get_rect()
            rl.bottomleft = (self.rabbitx, self.rabbity)
            rld = self.lapin_dodo[math.trunc(self.nbbg / 30 * 4)].get_rect()
            rld.bottomright = rl.bottomright
            screen.blit(self.lapin_dodo[math.trunc(self.nbbg / 30 * 4)], rld)
            if self.move >= 2:
                s = pygame.surface.Surface((1024, 768))
                s.set_alpha(self.alpha)
                screen.blit(s, (0, 0))
                self.alpha += 2
            if self.nbbg == 0 and self.move == 6:
                self.anim_3 = False
                self.move = 0
                self.platformer = self.prep_platformer
                self.runner = self.prep_runner
            elif self.nbbg == 0:
                self.move += 1
