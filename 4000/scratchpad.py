import pygame, os, sys
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((700, 100))
pygame.display.set_caption("First game")

screen = pygame.display.get_surface()
monkey_file_name = os.path.join("examples", "data", "chimp.bmp")
monkey_surface = pygame.image.load(monkey_file_name)
screen.blit(monkey_surface, (35, 40))

pygame.display.flip()


def sense(events):
    for event in events:
        if event.type == KEYDOWN and event.unicode == "s":
            screen_copy = screen.copy()
            screen_copy.fill(Color('black'))
            screen_copy.blit(monkey_surface, (0, 0))
            screen.blit(screen_copy, (0, 0))
        elif event.type == KEYDOWN and event.unicode == "d":
            screen_copy = screen.copy()
            screen_copy.fill(Color('black'))
            screen_copy.blit(monkey_surface, (35, 40))
            screen.blit(screen_copy, (0, 0))
        if event.type is QUIT:
            sys.exit(0)
        print(event)
        pygame.display.flip()


while True:
    sense(pygame.event.get())

