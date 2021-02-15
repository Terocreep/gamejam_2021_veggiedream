import pygame

class Colectible:
    def __init__(self, pose, sprit, tailleX, tailleY, name):
        self.sprite = pygame.image.load('images/' + sprit)
        self.sprite = pygame.transform.scale(self.sprite, (tailleX, tailleY))
        self.image = pygame.Surface((tailleX, tailleY))
        self.rect = self.image.get_rect()
        self.rect.move_ip(pose.getX(), pose.getY())
        self.name = name

    def recup(self, colectibles):
        colectibles.remove(self)
        return self.name
