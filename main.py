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
# TODO make the number of lists in the list depend on number of levels
target_images = [[], [], []]
# dictionary contain the number of each enemy difficulty to create on each level
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}
NUMBER_OF_TARGETS_ARRAY = [3, 3, 4]
level = 1
NUMBER_OF_LEVELS = 3
points = 0
shot = False
total_shots = 0
level_shots = 0
modes = {'freeplay': 0,
         'accuracy': 1,
         'timed': 2}
mode = 1
time_passed = 0
ammo = [27, 22, 38]
# values are in seconds
level_time = [20, 15, 25]
counter = 1
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


def draw_score():
    # creates texts that is ready to be placed on screen, the true value is for anti aliasing
    points_text = font.render(f'Points: {points}', True, 'black')
    screen.blit(points_text, (320, 660))
    shots_text = font.render(f'Total Shots: {total_shots}', True, 'black')
    screen.blit(shots_text, (320, 687))
    time_text = font.render(f'Time Elapsed: {time_passed}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == modes['freeplay']:
        mode_text = font.render(f'Freeplay!', True, 'black')
    elif mode == modes['accuracy']:
        mode_text = font.render(f'Ammo Remaining: {ammo[level - 1] - level_shots}', True, 'black')
    elif mode == modes['timed']:
        mode_text = font.render(f'Time Remaining: {level_time[level - 1] - time_passed}', True, 'black')
    screen.blit(mode_text, (320, 741))



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


"""make the targets move horizontal across the screen with different speeds"""
def move_level(coords):
    for i in range(NUMBER_OF_TARGETS_ARRAY[level - 1]):
        for j in range(len(coords[i])):
            my_coords = coords[i][j]
            # if at end of screen
            if my_coords[0] < -150:
                coords[i][j] = WIDTH, my_coords[1]
            else:
                coords[i][j] = (my_coords[0] - 2**i, my_coords[1])
    return coords


def draw_level(coords):
    # target_numbers = NUMBER_OF_TARGETS_ARRAY[level - 1]
    # # target hit box
    # target_rects = [[]] * target_numbers
    # TODO make the above code work and replace the if statements bellow
    if level == 1 or level == 2:
        target_rects = [[], [], []]
    else:
        target_rects = [[], [], [], []]
    # x loop
    for i in range(len(coords)):
        # y loop
        for j in range(len(coords[i])):
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] + 20, coords[i][j][1]), (60- i*12, 60 - i*12)))
            screen.blit(target_images[level-1][i], coords[i][j])
    return target_rects


def check_shot(targets, coords):
    # targets is the target_rects list created in draw_level
    global points
    mouse_pos = pygame.mouse.get_pos()
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            if targets[i][j].collidepoint(mouse_pos):
                # removes target from coords list
                coords[i].pop(j)
                # sets scoring system
                points += 10 + 10 * (i**2)
                # TODO add sounds for enemy hit
    return coords


# initialize enemy coordinates
# variate from tutorial so may cause errors
# TODO make the number of lists in the list depend on number of targets
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
                two_coords[i].append((WIDTH//(my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
            elif k == 2:
                three_coords[i].append((WIDTH//(my_list[i]) * j, 300 - (i * 100) + 30 * (j % 2)))


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
        target_boxes = draw_level(one_coords)
        one_coords = move_level(one_coords)
        if shot:
            one_coords = check_shot(target_boxes, one_coords)
            shot = False
    elif level == 2:
        target_boxes = draw_level(two_coords)
        two_coords = move_level(two_coords)
        if shot:
            two_coords = check_shot(target_boxes, two_coords)
            shot = False
    elif level == 3:
        target_boxes = draw_level(three_coords)
        three_coords = move_level(three_coords)
        if shot:
            three_coords = check_shot(target_boxes, three_coords)
            shot = False

    if level > 0:
        draw_gun()
        draw_score()
        # the tick command above makes this run at 60 fps so each loop is 1/60 a second
        # therefore this works as a clock
        if counter < 60:
            counter += 1
        else:
            counter = 1
            time_passed += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            if (0 < mouse_position[0] < WIDTH) and (0 < mouse_position[1] < HEIGHT - 200):
                shot = True
                total_shots += 1
                level_shots += 1
                # TODO make an ammo variable dependent on if in the

    # used to change to new level
    # TODO make the boxes multiply
    if target_boxes == [[], [], []] and level < NUMBER_OF_LEVELS:
        level_shots = -1 * (ammo[level - 1] - level_shots)
        time_passed = 0
        level += 1


    pygame.display.flip()

pygame.quit()
