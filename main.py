# TODO make all global variables get handed into the functions
# TODO make more things functions
# TODO make multiple files
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
level = 0
NUMBER_OF_LEVELS = 3
points = 0
shot = False
total_shots = 0
level_shots = 0
modes = {'freeplay': 0,
         'accuracy': 1,
         'timed': 2}
mode = 0
time_passed = 0
ammo = [27, 22, 38]
# values are in seconds
level_time = [20, 15, 25]
counter = 1
menu = True
game_over = False
pause = False
menu_img = pygame.image.load('assets/menus/mainMenu.png')
game_over_img = pygame.image.load('assets/menus/pause.png')
pause_img = pygame.image.load('assets/menus/gameOver.png')
best_freeplay = 0
best_ammo = 0
best_time = 0
clicked = False
write_values = False
target_boxes = None
resume_level = level
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


def draw_menu():
    global game_over, pause, mode, level, counter, total_shots, points, modes, menu
    global best_freeplay, best_ammo, best_time, write_values,clicked
    game_over = False
    pause = False
    screen.blit(menu_img, (0, 0))
    create_coords()

    # stuff for the buttons
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    freeplay_button = pygame.rect.Rect((170, 524), (260, 100))
    ammo_button = pygame.rect.Rect((475, 524), (260, 100))
    timed_button = pygame.rect.Rect((170, 661), (260, 100))
    reset_button = pygame.rect.Rect((475, 661), (260, 100))

    # rendering previous scores
    screen.blit(font.render(f'{best_freeplay}', True, 'black'), (340, 580))
    screen.blit(font.render(f'{best_ammo}', True, 'black'), (650, 580))
    screen.blit(font.render(f'{best_time}', True, 'black'), (350, 710))

    # checking for button presses
    if freeplay_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = modes['freeplay']
        level = 1
        counter = 0
        total_shots = 0
        points = 0
        menu = False
        clicked = True
    if ammo_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = modes['accuracy']
        level = 1
        counter = 0
        total_shots = 0
        points = 0
        menu = False
        clicked = True
    if timed_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = modes['timed']
        level = 1
        counter = 0
        total_shots = 0
        points = 0
        menu = False
        clicked = True
    if reset_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        best_freeplay = 0
        best_ammo = 0
        best_time = 0
        write_values = True
        clicked = True


def draw_game_over():
    global points, clicked, level, menu, total_shots, time_passed
    screen.blit(game_over_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()

    # creates hit boxes
    exit_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))

    screen.blit(font.render(f'{points}', True, 'black'), (640, 595))

    if exit_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        pygame.quit()
    if menu_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = 0
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        clicked = True


def draw_pause():
    global menu, level, pause, resume_level, clicked, points, total_shots, time_passed, level_shots
    screen.blit(pause_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()

    # creates hit boxes
    resume_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))

    # checks if clicked
    if resume_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = resume_level
        pause = False
    if menu_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = 0
        pause = False
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        clicked = True
        level_shots = 0


def draw_score():
    # creates texts that is ready to be placed on screen, the true value is for anti aliasing
    points_text = font.render(f'Points: {points}', True, 'black')
    screen.blit(points_text, (320, 660))
    shots_text = font.render(f'Shots Taken: {total_shots}', True, 'black')
    screen.blit(shots_text, (320, 687))
    time_text = font.render(f'Time Elapsed: {time_passed}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == modes['freeplay']:
        mode_text = font.render(f'Freeplay!', True, 'black')
    elif mode == modes['accuracy']:
        mode_text = font.render(f'Ammo Remaining: {ammo[level - 1] - level_shots}', True, 'black')
    elif mode == modes['timed']:
        mode_text = font.render(f'Time Remaining: {level_time[level - 1] - time_passed}', True, 'black')
    else:
        mode_text = font.render(f'ERROR', True, 'black')
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
def create_coords():
    global one_coords, two_coords, three_coords, NUMBER_OF_LEVELS, NUMBER_OF_TARGETS_ARRAY, targets, WIDTH
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

create_coords()
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

    if menu:
        level = 0
        draw_menu()
    elif game_over:
        level = 0
        draw_game_over()
    elif pause:
        level = 0
        draw_pause()
    else:
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

    # TODO put this in the above else statement and remove the if statement
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
            elif (670 < mouse_position[0] < 860) and (660 < mouse_position[1] < 715):
                resume_level = level
                pause = True
                clicked = True
            elif (670 < mouse_position[0] < 860) and (715 < mouse_position[1] < 760):
                menu = True
                level_shots = 0
                clicked = True
                level = 0
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
            clicked = False

    # used to change to new level
    # TODO make the boxes multiply
    if target_boxes == [[], [], []] and 0 < level < NUMBER_OF_LEVELS:
        level_shots = -1 * (ammo[level - 1] - level_shots)
        time_passed = 0
        level += 1
    # handles end game
    elif (level == NUMBER_OF_LEVELS and target_boxes == [[], [], [], []])\
            or (mode == modes['accuracy'] and level_shots == ammo[level - 1])\
            or (mode == modes['timed'] and time_passed == level_time[level - 1]):
        game_over = True
        if mode == modes['freeplay']:
            if time_passed < best_freeplay or best_freeplay == 0:
                best_freeplay = time_passed
                write_values = True
        elif mode == modes['accuracy'] and points > best_ammo:
            best_ammo = points
            write_values = True
        elif mode == modes['timed'] and points > best_time:
            best_time = points
            write_values = True

    pygame.display.flip()

pygame.quit()
