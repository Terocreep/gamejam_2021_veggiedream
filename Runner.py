from src.Player import Player
from src.Platform import Platform
from src.Objects import Saw, Bird, Carrot, GiantCarrot
import math
import pygame
import random

player = Player("", 400, 200)
gCarrot = GiantCarrot(2, 581, 128, 128)

class Runner:

    def __init__(self, level):

        self.speed = 6

        self.platforms_sol = []
        for i in range (0,16):
            self.platforms_sol.append(Platform(i*64, 709, "images/vide.png", False, False))

        self.x = 0

        #Genere un evenement aleatoire entre 2 et 3,5 secondes
        self.obstacles = []
        self.nb_frame = 0
        self.random_frame = random.randint(60,120)

        #Carrots
        self.carrots = []
        self.random_carrot_spawn = random.randint(40, 70)

        #Score
        self.score = 0

        #Collision
        self.enemy = []

        # backGroud for paralax
        self.background_images = []
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_4.png"),
                                                             (512, 384)))
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_6.png"),
                                                             (512, 384)))
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_8.png"),
                                                             (512, 384)))

        self.background_images[0] = pygame.transform.scale(self.background_images[0], (1024, 768))
        self.background_images[1] = pygame.transform.scale(self.background_images[1], (1024, 768))
        self.background_images[2] = pygame.transform.scale(self.background_images[2], (1024, 768))
        self.x1 = 0
        self.x2 = 0

        player.walking = True

    def update(self, x, y, screen):

        #Defilement du background
        back = self.background_images[0]
        rel_x = self.x2 % back.get_rect().width
        screen.blit(back, (rel_x - back.get_rect().width, 0))
        if rel_x < 1024:
            screen.blit(back, (rel_x, 0))

        back = self.background_images[1]
        rel_x = self.x1 % back.get_rect().width
        screen.blit(back, (rel_x - back.get_rect().width, 0))
        if rel_x < 1024:
            screen.blit(back, (rel_x, 0))

        back = self.background_images[2]
        rel_x = self.x % back.get_rect().width
        screen.blit(back, (rel_x - back.get_rect().width, 0))
        if rel_x < 1024:
            screen.blit(back, (rel_x, 0))

        self.x -= self.speed
        self.x1 -= self.speed/2
        self.x2 -= self.speed/3

        #Ajout de la Carrote Géante
        gCarrot.draw(screen)

        #Verfication de la collision
        player.die([], self.enemy, self.obstacles)

        #Deplacement du joueur
        if y == -1:
            player.jump(self.platforms_sol)
            player.update(self.platforms_sol)
        elif y == 1:
            player.velocity[0] = -2
            player.sneak(self.platforms_sol)
        else:
            player.update(self.platforms_sol)
        screen.blit(player.sprite, player.rect)

        #Ajout de carotte
        if self.nb_frame == self.random_carrot_spawn:
            h = random.randint(450, 677)
            self.carrots.append(Carrot(1030, h, 32, 32))
            self.random_carrot_spawn = random.randint(45, 70)

        for carrot in self.carrots:
            carrot.x -= self.speed
            if player.rect.x - 100 < carrot.x < player.rect.x + 100:
                if player.catchCarrot(self.carrots):
                    self.carrots.pop(self.carrots.index(carrot))
                    self.score += 1
            if carrot.x < carrot.width * -1:
                self.carrots.pop(self.carrots.index(carrot))
            carrot.draw(screen)

        #Ajout d'obstacles
        if self.nb_frame == self.random_frame:
            r = random.randint(0, 2)
            if r == 0:
                self.obstacles.append(Saw(1030, 645, 64, 64))
            elif r == 1:
                self.obstacles.append(Bird(1030, 450, 64, 32))

            self.nb_frame = 0
            self.random_frame = random.randint(60,80)

        for obstacle in self.obstacles:

            obstacle.x -= self.speed
            obstacle.draw(screen)

            if gCarrot.destroyObstacle(self.obstacles):
                print("DESTRUCTION !")

            if obstacle.x < obstacle.width * -1:
                self.obstacles.pop(self.obstacles.index(obstacle))

        self.nb_frame += 1
        self.speed = 6 + math.trunc(self.score/2)
