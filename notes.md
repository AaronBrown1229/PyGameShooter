# order of operations
## initial git setup
1. created github repo
2. made ReadMe file
3. cloned repo
4. cloned example project repo
5. made pycharm project in git folder
6. copied the assets folder into project folder
7. made .gitignore to ignore the venv .idea and example project

## setting up pygame
1. initalized pygame
2. created variables for the
    - fps
    - timer
    - font
    - window width
    - window height
3. set up a screen using width and height constants

## importing images
1. created arrays for each image type
    - bgs = background
    - banners
    - guns
2. created a variable called level that will keep track of the level we are on
3. created a for loop that will run depending on amount of levels to fill the image arrays

## creating background
1. made a bool variable called run
2. made a while loop based on run
3. made timer tick at fps
4. made screen black
5. drew the background and banner
6. made an end game condition based on pygame.QUIT
7. made screen redraw using flip
8. outside while loop called quit() to end program

## drawing gun
1. made a new function called draw gun
2. in main while loop if level is greater than 0 draw gun is called
3. draw gun gets the mouse_pos, gun position, and clicks
4. made an array holding the colours of lasers for each level
5. did geometry stuff to make gun fallow mouse
6. made it for gun inverses if on left side of screen
7. made it detect clicks and draw circles at the mouse if click happens
8. made gun scale down when imported

## setting starting positions of all targets
1. loaded the target images using a for loop and stored them in a list of lists, each inner list represents a level
2. made a dictionary that contains the number of each type to put on each level
3. made a draw level function that will place targets at the specified coords handed to it
4. made the initial cord for each level

## making targets move
1. made a new function called move_level
   - it takes coords as a argument
   - will move the target to the other side of the screen if off scree
   - if still on screen shift over at a rate dependent on level of target
   - returns new coords
2. called move cords after draw board and updated the appropriate coordinate set

## making shots
1. made new function called draw_level
   - it takes the targets and coords as arguments
   - if the mouse is position is on the hit box of a target the target is removed from the coords
   - increases the points
   - returns coords
2. made an if statement in each level's if statement that will run check_shot if a click occurred
3. made another event handler to set shot to true when the mouse is clicked

## advance level when all enemy are dead
1. made a simple if statement at end of run loop that checks if there are anymore target boxes
2. if there are no more target boxes and the level is less than number of levels advance

## draw text on score card
1. made function draw_score that will draw all the required stuff depending on mode
2. made a timer

# Things learned
1. can't make a list of lists by multipling
   - ie. can't do `x = [[]] * 3`
2. \ is a new line char allowing for statements to take up multiple lines