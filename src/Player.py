import pygame
import math
from pygame import mixer


pygame.display.set_mode((1024, 768))


class Player:
    def __init__(self, image, x, y):
        self.image = pygame.Surface((66, 64))
        self.image.fill((255, 255, 255))
        self.walkcount = 0
        self.health = 24
        self.max_health = 100
        self.imgs_falling = [
            pygame.transform.scale(pygame.image.load("images/lapin_falling_1.png"), (66, 64)),
            pygame.transform.scale(pygame.image.load("images/lapin_falling_2.png"), (66, 64)),
            pygame.transform.scale(pygame.image.load("images/lapin_falling_3.png"), (66, 64))
        ]
        self.imgs = [pygame.transform.scale(pygame.image.load("images/lapin_course_1.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_2.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_3.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_course_4.png"), (66, 64)),
                     pygame.transform.scale(pygame.image.load("images/lapin_stand.png"), (66, 64))]
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
        pygame.mixer.init()
        self.sound_jump = mixer.Sound('musics/jump_sound.ogg')

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

        if self.walkcount == 24:
            self.walkcount = 1

        self.img = self.imgs[math.trunc(self.walkcount/6)]

        if self.velocity[1] > 0:
            self.img = self.imgs_falling[math.trunc(self.walkcount / 8)]

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

    def jump(self, velocity, platforms):
        for p in platforms:
            if self.velocity[1] == 0 and not self.is_on(p) and not self.rect.colliderect(p.rect):
                self.is_falling = True
                self.velocity[1] = -velocity
                self.sound_jump.play()

    def gravity(self):
        self.velocity[1] += 2
        if self.velocity[1] > 40:
            self.velocity[1] = 40

    def die(self, platforms, enemys, obstacles):
        mort = False
        for p in platforms:
            if self.rect.x - 100 < p.rect.x < self.rect.x + 100:
                # si colision avec une platforme mortel
                if p.mortel and (self.is_on(p) or self.colliding_w_wall_left(p) or
                                 self.colliding_w_wall_right(p) or self.is_under(p)):
                    mort = True
        for e in enemys:
            m1 = pygame.mask.from_surface(self.sprite)
            m2 = pygame.mask.from_surface(e.sprite)
            if m1.overlap(m2, (self.rect.centerx - e.rect.centerx,
                               self.rect.centery - e.rect.centery)):
                if self.rect.colliderect(e.rect):
                    mort = True
        for o in obstacles:
            if self.rect.x - 100 < o.rect.x < self.rect.x + 100:
                m1 = pygame.mask.from_surface(self.sprite)
                m2 = pygame.mask.from_surface(o.sprite)

                if m1.overlap(m2, (self.rect.centerx - o.rect.centerx,
                                   self.rect.centery - o.rect.centery)):
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

    def addHealth(self, health):
        if self.max_health > self.health + health:
            self.health = self.health + health
        else:
            self.health = self.max_health

    def removeHealth(self, health):
        if self.health - health < 0:
            self.health = 0
        else:
            self.health = self.health - health

    def getHealth(self):
        return self.health

    def update_health_bar(self, screen):
        if self.health < 25:
            health_color = (200, 0, 0)
        elif self.health < 50:
            health_color = (213, 122, 0)
        else:
            health_color = (25, 137, 0)
        back_health_color = (106, 106, 106)

        position = [36, 36, self.health * 1.65 * 2, 22]
        back_position = [36, 36, self.max_health * 1.65 * 2, 22]

        pygame.draw.rect(screen, back_health_color, back_position)
        pygame.draw.rect(screen, health_color, position)
