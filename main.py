import pygame

pygame.init()
pygame.display.init()
pygame.display.set_mode((800, 600), pygame.RESIZABLE)

import menu

menu.loop()