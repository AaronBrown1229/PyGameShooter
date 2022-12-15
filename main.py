import pygame
import math

"""setting up pygame"""
pygame.init()
fps = 60
timer = pygame.time.Clock()
# declaring the font to use. The first argument is the path to the font being used the second is its size
font = pygame.font.Font('assets/font/myFont.ttf', 32)

# screen size
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

"""importing images"""
# lists to hold assists
bgs = []
banners = []
guns = []
level = 0
# used to populate the asset lists with images
# range is 1,4 because there are three levels
for i in range(1, 4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/bgs/{i}.png'))
    guns.append(pygame.image.load(f'assets/bgs/{i}.png'))
