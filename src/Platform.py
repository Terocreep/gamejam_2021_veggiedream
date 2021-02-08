import pygame


class Platform:
    def __init__(self, x, y, width, height):
        print("init")
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)