import os
import pygame


class Saw(object):

    img = [pygame.image.load(os.path.join('images', 'SAW0.PNG')), pygame.image.load(os.path.join('images', 'SAW1.PNG')), pygame.image.load(os.path.join('images', 'SAW2.PNG')), pygame.image.load(os.path.join('images', 'SAW3.PNG'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.frame_count = 0

    def draw(self, screen):
        self.rect = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.frame_count >= 8:
            self.frame_count = 0
        screen.blit(pygame.transform.scale(self.img[self.frame_count // 2], (64, 64)), (self.x, self.y))
        self.frame_count += 1
        #pygame.draw.rect(screen, (255,0,0), self.rect, 2)


class Bird(Saw):
    img = pygame.image.load(os.path.join('images', 'bird.png'))

    def draw(self, screen):
        self.rect = (self.x, self.y, self.width, self.height)
        screen.blit(pygame.transform.scale(self.img, (64, 32)), (self.x, self.y))
        #pygame.draw.rect(screen, (255,0,0), self.rect, 2)


class Carrot(Saw):
    img = pygame.image.load(os.path.join('images', 'carrot.png'))

    def draw(self, screen):
        self.rect = (self.x, self.y, self.width, self.height)
        screen.blit(pygame.transform.scale(self.img, (32, 32)), (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
