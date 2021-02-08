import pygame

pygame.init()

from gamejam-2021.vue import Vue


def main():
    screen = Vue()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.quit():
                running = False


if __name__ == '__main__':
    main()
