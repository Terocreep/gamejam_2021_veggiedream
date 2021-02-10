from src.Player import Player
from src.Platform import Platform
from src.Objects import Saw, Bird, Carrot
import pygame
import random

player = Player("", 400, 200)


class Runner:

    def __init__(self, level):

        self.speed = 6

        self.platforms = []
        for i in range (0,16):
            self.platforms.append(Platform(i*64, 709, "images/vide.png", False, False))

        self.background_floor = pygame.image.load("images/floor.png").convert()
        self.background_forest = pygame.image.load("images/forest.png").convert()
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
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_1.png"),
                                                             (1024, 768)))
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_6.png"),
                                                             (1024, 768)))
        self.background_images.append(pygame.transform.scale(pygame.image.load("images/background_layers/Layer_8.png"),
                                                             (1024, 768)))

        player.walking = True

    def update(self, x, y, screen):

        #Defilement du background
        for i in range(1, 4):
            back = self.background_images[i-1]
            rel_x = (self.x - (6-i)) % back.get_rect().width
            screen.blit(back, (rel_x - back.get_rect().width, 0))
            if rel_x < 1024:
                screen.blit(back, (rel_x, 0))

        self.x -= 6

        #Verfication de la collision
        player.die(self.platforms, self.enemy, self.obstacles)

        #Deplacement du joueur
        if y == -1:
            player.jump(self.platforms)
            player.update(self.platforms)
        elif y == 1:
            player.velocity[0] = -2
            player.sneak(self.platforms)
        else:
            player.update(self.platforms)
        screen.blit(player.sprite, player.rect)

        if self.nb_frame == self.random_carrot_spawn:
            h = random.randint(400, 560)
            self.carrots.append(Carrot(1000, h, 32, 32))
            self.random_carrot_spawn = random.randint(45, 70)

        for carrot in self.carrots:
            carrot.x -= 9
            carrot.draw(screen)
            if player.catchCarrot(self.carrots):
                self.carrots.pop(self.carrots.index(carrot))
                self.score += 1
                print(self.score)
            if carrot.x < carrot.width * -1:
                print("Carotte supprimé")
                self.carrots.pop(self.carrots.index(carrot))

        #Ajout d'obstacles
        if self.nb_frame == self.random_frame:
            r = random.randint(0,2)
            if r == 0:
                self.obstacles.append(Saw(800, 560, 64, 64))
            elif r == 1:
                self.obstacles.append(Bird(800, 400, 64, 32))

            self.nb_frame = 0
            self.random_frame = random.randint(60,80)

        for obstacle in self.obstacles:
            obstacle.x -= 9
            obstacle.draw(screen)
            if obstacle.x < obstacle.width * -1:
                print("Obstacle supprimé")
                self.obstacles.pop(self.obstacles.index(obstacle))

        self.nb_frame += 1
