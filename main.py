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
target_images = [[], [], []]
# dictionary contain the number of each enemy difficulty to create on each level
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}
NUMBER_OF_TARGETS_ARRAY = [3, 3, 4]
level = 3
NUMBER_OF_LEVELS = 3
# used to populate the asset lists with images
# range is 1,4 because there are three levels
for i in range(1, NUMBER_OF_LEVELS + 1):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    # makes gun smaller
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'), (100, 100)))
    # loads the targets
    number_of_targets = NUMBER_OF_TARGETS_ARRAY[i - 1]
    # for target in folder
    for j in range(1, number_of_targets + 1):
        # will make images smaller for each level
        target_images[i-1].append(pygame.transform.scale(
            pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j*18), 80 - (j*12))))


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


def draw_level(coords):
    target_numbers = NUMBER_OF_TARGETS_ARRAY[level - 1]
    # target hit box
    target_rects = [[]] * target_numbers
    # x loop
    for i in range(len(coords)):
        # y loop
        for j in range(len(coords[i])):
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] + 20, coords[i][j][1]), (60- i*12, 60 - i*12)))
            screen.blit(target_images[level-1][i], coords[i][j])
    return target_rects


# initialize enemy coordinates
# variate from tutorial so may cause errors
# one_coords = [[], [], []]
# two_coords = [[], [], []]
# three_coords = [[], [], [], []]
# for i in range(3):
#     my_list = targets[1]
#     for j in range(my_list[i]):
#         one_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
# for i in range(3):
#     my_list = targets[2]
#     for j in range(my_list[i]):
#         two_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
# for i in range(4):
#     my_list = targets[3]
#     for j in range(my_list[i]):
#         three_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 100) + 30 * (j % 2)))
one_coords = [[], [], []]
two_coords = [[], [], []]
three_coords = [[], [], [], []]
for k in range(NUMBER_OF_LEVELS):
    for i in range(NUMBER_OF_TARGETS_ARRAY[k]):
        my_list = targets[k+1]
        for j in range(my_list[i]):
            if k == 0:
                # makes them staggered with j%2
                one_coords[i].append((WIDTH//(my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
            elif k == 1:
                two_coords[i].append((WIDTH//(my_list[i]) * j, 200 - (i * 150) + 30 * (j % 2)))
            elif k == 2:
                three_coords[i].append((WIDTH//(my_list[i]) * j, 100 - (i * 100) + 30 * (j % 2)))


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

    if level == 1:
        draw_level(one_coords)
    elif level == 2:
        draw_level(two_coords)
    elif level == 3:
        draw_level(three_coords)

    if level > 0:
        draw_gun()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
