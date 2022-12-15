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
8. outside while loop caled quit() to end program

## drawing gun
1. made a new function called draw gun
2. in main while loop if level is greater than 0 draw gun is called
3. draw gun gets the mouse_pos, gun position, and clicks
4. made an array holding the colours of lasers for each level
5. did geometry stuff to make gun fallow mouse
6. made it for gun inverses if on left side of screen
7. made it detect clicks and draw circles at the mouse if click happens