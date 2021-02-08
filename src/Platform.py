import pygame


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load('images/sol_jour.png')
        self.sprite = pygame.transform.scale(self.sprite, (68, 64))
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)