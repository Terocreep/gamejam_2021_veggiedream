from src.Player import Player
from src.Platform import Platform


player = Player("")



class Platformer:
    def __init__(self, level):
        self.platforms = []
        self.platforms.append(Platform(0, 700, 100, 100))
        self.platforms.append(Platform(200, 700, 100, 100))
        self.platforms.append(Platform(400, 700, 100, 100))

    def update(self, x, y, screen):
        player.velocity = [200 * 0.033 * x, 200 * 0.033 * y]
        player.update()
        for p in self.platforms:
            screen.blit(p.image, (p.x, p.y))
        screen.blit(player.image, player.rect)
