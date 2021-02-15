import os
import pygame
import math


class Saw(object):

    img = [
        pygame.image.load(os.path.join('images', 'SAW0.PNG')),
        pygame.image.load(os.path.join('images', 'SAW1.PNG')),
        pygame.image.load(os.path.join('images', 'SAW2.PNG')),
        pygame.image.load(os.path.join('images', 'SAW3.PNG'))
    ]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.frame_count = 0
        self.sprite = self.img[0]

    def draw(self, screen):
        self.rect = pygame.rect.Rect(self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.frame_count >= 8:
            self.frame_count = 0
        self.sprite = pygame.transform.scale(self.img[self.frame_count // 2], (80, 80))
        screen.blit(self.sprite, (self.x, self.y))
        self.frame_count += 1


class Bird(Saw):
    img = [pygame.image.load(os.path.join('images', 'bird.png'))]

    def draw(self, screen):
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        screen.blit(pygame.transform.scale(self.img[0], (64, 32)), (self.x, self.y))


class Carrot(Saw):
    img = [pygame.image.load(os.path.join('images', 'carrote.png'))]

    def draw(self, screen):
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        screen.blit(pygame.transform.scale(self.img[0], (32, 32)), (self.x, self.y))


class GiantCarrot(Saw):
    img = [
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'carotte_course_1.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'carotte_course_2.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'carotte_course_3.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'carotte_course_4.png')), True, False)
    ]

    # Sprit of giant carrot
    gsprit = [
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'coup_carotte_1.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'coup_carotte_2.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'coup_carotte_3.png')), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'coup_carotte_4.png')), True, False)

    ]
    hit_obstacle = False
    mx = 128
    my = 128

    def draw(self, screen,):
        if self.hit_obstacle:
            if self.frame_count >= 16:
                self.frame_count = 0
                self.hit_obstacle=False

            screen.blit(pygame.transform.scale(self.img[math.trunc(self.frame_count / 4)], (self.mx, self.my)),
                        (0, 709 - self.my))
            screen.blit(pygame.transform.scale(self.gsprit[math.trunc(self.frame_count / 4)], (self.mx, self.my)),
                        (0, 709 - self.my))
        else:
            self.rect = pygame.rect.Rect(self.x, 709 - self.my, self.mx, self.my)
            if self.frame_count >= 16:
                self.frame_count = 0
            screen.blit(pygame.transform.scale(self.img[math.trunc(self.frame_count / 4)], (self.mx, self.my)),
                        (0, 709 - self.my))

        self.frame_count += 1

    def hit(self, screen):
        self.frame_count = 0
        self.hit_obstacle = True

    def destroyObstacle(self, obstacles):
        mort = False
        for o in obstacles:
            if self.rect.x - 10 < o.rect.x < self.rect.x + 50:
                if self.rect.colliderect(o.rect):
                    mort = True
        return mort
