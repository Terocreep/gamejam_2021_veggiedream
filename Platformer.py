from src.Player import Player
from src.Platform import Platform


lapin = Player("")
platforms = []


class Platformer:
    def __init__(self,screen, level):
        self.screen = screen
        platforms[len(platforms)] = Platform(700, 0, 100, 100)