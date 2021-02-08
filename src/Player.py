import pygame


class Player:
    def __init__(self, image):
        self.image = pygame.Surface((64, 64))
        self.img = pygame.image.load("images/lapin_4p.png")
        self.sprite = pygame.transform.flip(self.img, False, False)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.is_falling = True

    def update(self, platforms):
        # self.rect.move_ip(*self.velocity)
        if self.velocity[0] > 0:
            self.sprite = pygame.transform.flip(self.img, False, False)
        elif self.velocity[0] < 0:
            self.sprite = pygame.transform.flip(self.img, True, False)
        self.is_falling = True
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        for platform in platforms:
            if self.is_on(platform):
                self.rect.bottom = platform.rect.top
                self.velocity[1] = 0
                self.is_falling = False

        if self.is_falling:
            self.gravity()

    def is_on(self, platform):
        return self.rect.colliderect(platform.rect) and \
               ((platform.rect.x <= self.rect.x <= platform.rect.x + platform.rect.width) or \
               (platform.rect.x <= self.rect.x + self.rect.width <= platform.rect.x + platform.rect.width)) and \
               (platform.rect.y <= self.rect.bottom <= platform.rect.y + 40)

    def jump(self, platforms):
        for p in platforms:
            if self.velocity[1] == 0 and not self.is_on(p):
                self.velocity[1] = -31

    def gravity(self):
        self.velocity[1] += 2
