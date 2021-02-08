import pygame


class Player:
    def __init__(self, image):
        print("init")
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)