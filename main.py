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
level = 1
# used to populate the asset lists with images
# range is 1,4 because there are three levels
for i in range(1, 4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    guns.append(pygame.image.load(f'assets/guns/{i}.png'))


def draw_gun():
    mouse_pos = pygame.mouse.get_pos()
    # sets the gun position at the top of banner
    gun_point = (WIDTH/2, HEIGHT - 200)
    # sets the colour of lasers when player clicks
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()

    """fancy geometry stuff"""
    # prevents divide by 0, else set a very large native int
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1])/(mouse_pos[0] - gun_point[0])
    else:
        slope = -10000000
    angle = math.atan(slope)
    rotation = math.degrees(angle)

    # if the mouse is on the left side of the screen inverse the gun image
    if mouse_pos[0] < WIDTH/2:
        # image, x direction flip, y direction flip
        gun = pygame.transform.flip(guns[level - 1], True, False)
        # if player is looking at banner
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH/2 - 90, HEIGHT - 250))
            if clicks[0]:
                # draws a small circle with radius 5 to check if mouse clicks are registered
                pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)
    else:
        # else don't flip gun
        gun = guns[level - 1]
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH/2 - 30, HEIGHT - 250))
            if clicks[0]:
                # draws a small circle with radius 5 to check if mouse clicks are registered
                pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)


"""game loop"""
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    # draws the background
    # gets the level background and places it in the top left corner
    screen.blit(bgs[level - 1], (0, 0))
    # draws the banner 200 from bottom because that is the height of the image
    screen.blit(banners[level - 1], (0, HEIGHT - 200))

    if level > 0:
        draw_gun()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
