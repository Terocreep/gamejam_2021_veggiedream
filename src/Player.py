import pygame


class Player:
    def __init__(self, image):
        print("init")
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.is_falling = True

    def update(self, platforms):
        # self.rect.move_ip(*self.velocity)
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
               (platform.rect.x <= self.rect.x + self.rect.width <= platform.rect.x + platform.rect.width))

    def jump(self, platforms):
        for p in platforms:
            if self.velocity[1] == 0 and not self.is_on(p):
                self.velocity[1] = -31

    def gravity(self):
        self.velocity[1] += 2
