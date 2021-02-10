import pygame


class Platform:
    def __init__(self, x, y, img, traversable, mortel):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(img)
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.velocity = [0, 0]
        self.traversable = traversable
        self.mortel = mortel


def update(self):
        self.rect.move_ip(*self.velocity)