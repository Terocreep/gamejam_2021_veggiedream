import pygame
import math


pygame.display.set_mode((1024, 768))


class Player:
    def __init__(self, image, x, y):
        self.image = pygame.Surface((66, 64))
        self.image.fill((255, 255, 255))
        self.walkcount = 0
        self.dust = []
        self.imgs = [pygame.transform.scale(pygame.image.load("images/lapin_course_1.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_2.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_3.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_4.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_stand.png"), (66,64))]
        self.img = self.imgs[math.trunc(self.walkcount/5)]
        self.sprite = pygame.transform.flip(self.img, False, False)
        self.rect = self.sprite.get_rect()
        self.velocity = [0, 0]
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.walking = False
        self.is_falling = True

    def sneak(self, platforms):
        self.is_falling = True
        for platform in platforms:
            if self.is_on(platform) and platform.traversable:
                self.rect.y += 6
                self.is_falling = False
            if self.is_on(platform) and not platform.traversable:
                self.rect.bottom = platform.rect.top
                self.velocity[1] = 0
                self.is_falling = False
            if self.colliding_w_wall_right(platform) and not platform.traversable:
                self.rect.right = platform.rect.left
                self.velocity[0] = 0
            if self.colliding_w_wall_left(platform) and not platform.traversable:
                self.rect.left = platform.rect.right
                self.velocity[0] = 0
            if self.is_under(platform) and not platform.traversable:
                self.rect.top = platform.rect.bottom
                self.velocity[1] = 0

        if self.is_falling:
            self.velocity[1] += 8
            self.gravity()
            self.rect.y += self.velocity[1]
        self.rect.x += self.velocity[0]
        self.velocity[0] = 0
        self.sprite = self.imgs[4]

    def update(self, platforms):
        self.is_falling = True

        for platform in platforms:
            if self.is_on(platform):
                self.rect.bottom = platform.rect.top
                self.velocity[1] = 0
                self.is_falling = False
            if self.colliding_w_wall_right(platform) and not platform.traversable:
                self.rect.right = platform.rect.left
                self.velocity[0] = 0
            if self.colliding_w_wall_left(platform) and not platform.traversable:
                self.rect.left = platform.rect.right
                self.velocity[0] = 0
            if self.is_under(platform) and not platform.traversable:
                self.rect.top = platform.rect.bottom
                self.velocity[1] = 0

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.is_falling:
            self.gravity()

        if self.velocity[0] != 0 or self.walkcount != 1 or self.walking:
            self.walkcount += 1

        if self.walkcount == 20:
            self.walkcount = 1

        self.img = self.imgs[math.trunc(self.walkcount/5)]

        if self.is_falling:
            self.img = self.imgs[math.trunc(self.walkcount / 5)]

        if self.walking:
            self.sprite = pygame.transform.flip(self.img, False, False)
        elif self.velocity[0] > 0:
            self.sprite = pygame.transform.flip(self.img, False, False)
        elif self.velocity[0] < 0:
            self.sprite = pygame.transform.flip(self.img, True, False)
        else:
            self.sprite = self.imgs[4]

    def is_on(self, platform):
        return platform.rect.colliderect(self.rect.x + 1, self.rect.y + self.rect.h + self.velocity[1], self.rect.w - 2, 1)

    def is_under(self, platform):
        return platform.rect.colliderect(self.rect.x + 1, self.rect.y + self.velocity[1], self.rect.w - 2, 1)

    def colliding_w_wall_right(self, platform):
        return platform.rect.colliderect(self.rect.x + self.rect.w + self.velocity[0], self.rect.y + 1, 1, self.rect.h - 2)

    def colliding_w_wall_left(self, platform):
        return platform.rect.colliderect(self.rect.x + self.velocity[0], self.rect.y + 1, 1, self.rect.h - 2)

    def jump(self, platforms):
        for p in platforms:
            if self.velocity[1] == 0 and not self.is_on(p):
                self.velocity[1] = -31

    def gravity(self):
        self.velocity[1] += 2
        if self.velocity[1] >40:
            self.velocity[1] = 40

    def die(self, platforms, enemys, obstacles):
        mort = False
        for p in platforms:
            # si colision avec une platforme mortel
            if self.rect.colliderect(p.rect) and p.mortel:
                mort = True
        for e in enemys:
            if self.rect.colliderect(e.rect):
                mort = True
        for o in obstacles:
            if self.rect.colliderect(o.rect):
                mort = True
        if mort:
            # réspawn aux coordonée
            self.rect.x = self.x
            self.rect.y = self.y
            # reset vélocité
            self.velocity[0] = 0
            self.velocity[1] = 0
        return mort

    def catchCarrot(self, carrots):
        catch = False
        for c in carrots:
            if self.rect.colliderect(c.rect):
                catch = True
        return catch

    def setCoordonneeRespawn(self, x, y):
        self.x = x
        self.y = y
