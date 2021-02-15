from src.Player import Player
from src.Platform import Platform
from src.Objects import Saw, Bird, Carrot, GiantCarrot
import math
import pygame
import random
from pygame import mixer
from src.Score import Score

player = Player("", 400, 200)
gCarrot = GiantCarrot(0, 581, 128, 128)

class Runner:

    def __init__(self):

        self.speed = 6

        self.platforms_sol = []
        for i in range (0,16):
            self.platforms_sol.append(Platform(i*64, 709, "images/vide.png", False, False))

        self.x = 0

        self.score = Score("")

        # Music
        pygame.mixer.init()

        #Genere un evenement aleatoire entre 2 et 3,5 secondes
        self.obstacles = []
        self.nb_frame = 0
        self.nb_frame_carrot = 0
        self.random_frame = random.randint(60,120)

        #Carrots
        self.carrots = []
        self.random_carrot_spawn = random.randint(40, 70)

        # Score display
        self.score_value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 34)
        self.txtX = 950
        self.txtY = 10

        self.cadre = pygame.transform.scale(pygame.image.load("images/health_bar.png"), (402, 66))

        # Game Over
        self.game_over = False

        # Collision and enemy
        self.gx = 128
        self.gy = 128
        self.gCarrot = GiantCarrot(0, 709 - self.gy, self.gx, self.gy)
        self.enemy = [self.gCarrot]

        # backGround for paralax
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

    def play_music(self, pb):
        mixer.music.load('musics/background_runner.ogg')
        if pb:
            mixer.music.play(-1)
        else:
            mixer.music.stop()

    def set_player(self, username):
        self.score = Score(username)
        self.score.newVar("meurt", -10)
        self.score.newVar("carrote", 5)

    def update(self, x, y, screen):

        self.enemy = [self.gCarrot]

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
        self.gCarrot.draw(screen)

        #Verfication de la collision
        if player.die([], [], self.obstacles) or player.rect.x <= self.enemy[0].mx:
            player.removeHealth(20)
            self.score.execVar("meurt")
            player.rect.x = player.x
            player.rect.y = player.y
            player.velocity[0] = 0
            player.velocity[1] = 0
            if player.health <= 0:
                self.score.finPartie()
                self.game_over = True
                player.health = 50

        #Deplacement du joueur
        if y == -1:
            player.jump(25, self.platforms_sol, True)
            player.update(self.platforms_sol)
        elif y == 1:
            player.velocity[0] = -2
            player.sneak(self.platforms_sol)
        else:
            player.update(self.platforms_sol)
        screen.blit(player.sprite, player.rect)

        #Ajout de carotte
        if self.nb_frame_carrot == self.random_carrot_spawn:
            h = random.randint(500, 675)
            self.carrots.append(Carrot(1030, h, 32, 32))
            self.nb_frame_carrot = 0
            if self.score_value < 5:
                self.random_carrot_spawn = random.randint(40, 60)
            elif 5 <= self.score_value <= 7:
                self.random_carrot_spawn = random.randint(30, 40)
            else:
                self.random_carrot_spawn = random.randint(15, 30)

        for carrot in self.carrots:
            isCatched = False

            carrot.x -= self.speed
            if player.rect.x - 100 < carrot.x < player.rect.x + 100:
                if player.catchCarrot(self.carrots):
                    self.score_value += 1
                    isCatched = True
                    player.addHealth(1)
                    self.score.execVar("carrote")
            if carrot.x < self.gCarrot.rect.x + 100:
                if self.gCarrot.rect.colliderect(carrot.rect):
                    self.gCarrot.mx += 5
                    self.gCarrot.my += 5
                    self.gCarrot.rect.x += 5
                    self.gCarrot.rect.y += 5
                    self.enemy = [self.gCarrot]
                    isCatched = True

            if carrot.x < carrot.width * -1:
                self.carrots.pop(self.carrots.index(carrot))
            if isCatched:
                self.carrots.pop(self.carrots.index(carrot))
            carrot.draw(screen)

        #Ajout d'obstacles
        if self.nb_frame == self.random_frame:
            r = random.randint(0, 2)
            r1 = random.randint(0, 2)
            h = random.randint(450, 515)

            if r == 0:
                self.obstacles.append(Saw(1030, 629, 80, 80))
            elif r == 1:
                self.obstacles.append(Bird(1030, h, 64, 32))
                if r1 == 0 and self.score_value > 20:
                    self.obstacles.append(Saw(1110, 629, 80, 80))
                elif r1 == 1 and self.score_value > 20:
                    self.obstacles.append(Bird(1100, h, 64, 32))

            self.nb_frame = 0
            if self.score_value < 20:
                self.random_frame = random.randint(40, 60)
            elif 20 <= self.score_value <= 35:
                self.random_frame = random.randint(30, 47)
            else:
                self.random_frame = random.randint(20, 37)

        for obstacle in self.obstacles:

            obstacle.x -= self.speed
            obstacle.draw(screen)

            if self.gCarrot.destroyObstacle(self.obstacles):
                self.gCarrot.hit(screen)
                self.obstacles.pop(self.obstacles.index(obstacle))

            # Ajout de la Carrote Géante
            self.gCarrot.draw(screen)

            if obstacle.x < obstacle.width * -1:
                self.obstacles.pop(self.obstacles.index(obstacle))

        score = self.font.render(str(self.score_value), True, (255, 255, 255))
        screen.blit(score, (self.txtX, self.txtY))

        self.nb_frame += 1
        self.nb_frame_carrot += 1
        self.speed = 6 + math.trunc(self.score_value / 5)

        screen.blit(self.cadre, (0, 0))
        player.update_health_bar(screen)

