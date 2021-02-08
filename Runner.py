from src.Player import Player
from src.Platform import Platform


player = Player("")


class Runner:
    def __init__(self, level):
        self.platforms = []
        self.platforms.append(Platform(0, 700))
        self.platforms.append(Platform(200, 700))
        self.platforms.append(Platform(400, 700))

    def update(self, x, y, screen):
        player.velocity[0] = 200 * 0.033 * x
        if y == -1:
            player.jump(self.platforms)
        player.update(self.platforms)
        for p in self.platforms:
            screen.blit(p.image, (p.x, p.y))
        screen.blit(player.sprite, player.rect)