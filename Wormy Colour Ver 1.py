# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

#LAVAN SURENDRA, ROBERT MIRANDA, SIMON BRIGGS, AKSHAT REGANI

#SIMON BRIGGS START
import random, pygame, sys  #Importing Modules that will be used throughout the code
from pygame.locals import *  #Importing Graphic functions

FPS = 15  #Setting Frames Per Second, how often the game screen will refresh
WINDOWWIDTH = 640  #Setting dimensions of Graphics Window, this case Width
WINDOWHEIGHT = 480  #Setting dimensions of Graphics Window, this case Height
CELLSIZE = 20  #Setting how wide each 'square' that the Worm passes through will be
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(
  WINDOWWIDTH / CELLSIZE
)  #Cellwidth is an int of width/cellsize, so that all cells fit on screen
CELLHEIGHT = int(
  WINDOWHEIGHT / CELLSIZE
)  #Cellheight is an int of height/cellsize, so that all cells fit on screen

#             R    G    B
#Setting the value of each colour, so that instead of typing in the RGB values just add in the variable
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 115, 115 )
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
DARKORANGE = (255, 143, 0)
ORANGE = (255, 177, 77)
DARKPURPLE = (240, 0, 255 )
PURPLE = (246, 102, 255)
YELLOW = (251, 254, 85) 
DARKYELLOW = (246, 102, 255 )
DARKCYAN = (0, 255, 209)
CYAN = (105, 255, 253)
DARKBLUE = (0, 81, 255 )
BLUE = (111, 157, 255 ) 
DARKPINK = (255, 0, 197)
PINK = (255, 115, 223)
BGCOLOR = BLACK  #Black defined already on line 24

#Setting direction variables, so that don't need to worry about forgetting to make it a string
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


#
#Starting main function, where game will be run
def main():
  #Setting Global Variables that can be used anywhere in the function
  global FPSCLOCK, DISPLAYSURF, BASICFONT

  pygame.init()  #A function from the pygame module, starts the game.
  FPSCLOCK = pygame.time.Clock(
  )  #Setting FPSCLOCK to a function from pygame, which creates an object to track time
  DISPLAYSURF = pygame.display.set_mode(
    (WINDOWWIDTH, WINDOWHEIGHT)
  )  #Setting DISPLAYSURF to be the object that displays a visible game screen.
  BASICFONT = pygame.font.Font(
    'freesansbold.ttf',
    18)  #Setting the game font to BASICFONT with a function from pygame.
  pygame.display.set_caption(
    'Wormy')  #Defining what the name of the display will be.

  showStartScreen()  #Calling a function made below, which executes a script that launches the game and runs a start up sequence
  mode = drawMenuButtons()

  if mode == "normal":  #Always True

    # this while loop needs to be changed to an if statement to check which value was returned by the user pressing a button to choose the difficulty
    # depedning on which button was pressed a different rungame() function will be called

    runGame()  #Calls function 'runGame' which runs the actual game
    # we need two rungame functions, one for the regular mode and one for our changed mode
    showGameOverScreen(
    )  #Once runGame is returned, then the game over screen is shown. This way it is shown once the player loses the game.
  
  #else:
    #runGameHard()


#SIMON BRIGGS END


#LAVAN SURENDRA START
def runGame():
  # Set a random start point.
  startx = random.randint(5, CELLWIDTH - 6)
  starty = random.randint(5, CELLHEIGHT - 6)
  # Using a dictionary to define the coordinates of the snake, along with the next two body portions of the snake in the x direction (this means that the snake starts with 3 parts)
  wormCoords = [{
    'x': startx,
    'y': starty
  }, {
    'x': startx - 1,
    'y': starty
  }, {
    'x': startx - 2,
    'y': starty
  }]
  #the snakes original direction is defined to be towards the right
  direction = RIGHT

  # Starting the apple in a random place by calling the getRandomLocation() function
  apple = getRandomLocation()

  while True:  # main game loop which will run until the return statement occurs
    for event in pygame.event.get(
    ):  # event handling loop which iterates through each event that occurs
      # If the type of the event is quit the program will call the terminate() function
      if event.type == QUIT:
        terminate()
# If the user presses a key the KEYDOWN event type will be triggered
      elif event.type == KEYDOWN:

        # a nested if statement to determine whether the pressed key was a (for WASD controls) or the left arrow key (for arrow controls). If the direction is opposite to the key press it will not change the direction of the snake but otherwise this will change the direction of the snake to left
        if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
          direction = LEFT

# a nested if statement to determine whether the pressed key was d (for WASD controls) or the right arrow key (for arrow controls). If the direction is opposite to the key press it will not change the direction of the snake but otherwise this will change the direction of the snake to right
        elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
          direction = RIGHT

# a nested if statement to determine whether the pressed key was w (for WASD controls) or the up arrow key (for arrow controls). If the direction is opposite to the key press it will not change the direction of the snake but otherwise this will change the direction of the snake to up
        elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
          direction = UP

# a nested if statement to determine whether the pressed key was a (for WASD controls) or the left arrow key (for arrow controls). If the direction is opposite to the key press it will not change the direction of the snake but otherwise this will change the direction of the snake to down
        elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
          direction = DOWN

# a nested if statement to determine whether the pressed key was the escape key. If this is the case it'll call the terminate function to end the game
        elif event.key == K_ESCAPE:
          terminate()

    # check if the worm has the edge by comparing the position of the head with the edge of the frame. Cellwidth and cellheight are the maximum dimensions of the games frame whereas the -1 positions are associated with the minimum positions of the games frame
    if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD][
        'x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD][
          'y'] == CELLHEIGHT:
      return  # game over if this occurs

#  This loop goes through each of the body positions defined in the wormcords dictionary and the if statement checks if the coordinates of the head are matching with the coordinates of the body. If this occurs the game ends as the worm has hit itself
    for wormBody in wormCoords[1:]:
      if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody[
          'y'] == wormCoords[HEAD]['y']:
        return  # game over

    # this if statement checks if worm has eaten an apple by seeing if it's coordinates match with the apples coordinates, if this is the case the worms tail segment isn't removed
    if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple[
        'y']:
      # don't remove worm's tail segment, and since the worm is moved by constantly adding head segments and removing tail segments, this effectively makes the worm one tile longer
      apple = getRandomLocation(
      )  # set coordinates fora new apple positon somewhere in the games frame (which will later be passed on to the drawApple function)
    else:
      del wormCoords[-1]
# If no apple is contacted then the lastmost segment of the worm is removed, and since a new head segment is added in the portion of code below, this makes the worm appear to be moving.

# move the worm by adding a segment in the direction it is moving. Each of the if and else if conditions define a new head at the coordinates in front of the current head depending on which direction the worm is currently facing.
    if direction == UP:
      newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
      newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
      newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
    elif direction == RIGHT:
      newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
# Once the new head is defined it is then added into the dictionary containing the worm's body coordinates. Then using other functions, the grid is redrawn, along with the worm (based on the new worm coordinates) and the apple (based on the apple coordinates). The score is also updated by subtracting the original number of body pieces (3) by the current number of body pieces. Finally the display is updated
    wormCoords.insert(0, newHead)
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    colourScore = len(wormCoords) - 3
    drawWorm(wormCoords)
    drawApple(apple)
    drawScore(len(wormCoords) - 3)
    pygame.display.update()
    # The FPS clock is ticked forward to update it
    FPSCLOCK.tick(FPS)


#LAVAN SURENDRA END


#AKSHAT REGANI START
def drawPressKeyMsg():
  pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY) 
  #This variable holds the Text (image format) which is rendered with a font in this format            font.render("message", True,colour)
  pressKeyRect = pressKeySurf.get_rect() #Creates a rectangle with the text image in it
  pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)#Gives a size to the rectangle and postion topleft
  DISPLAYSURF.blit(pressKeySurf, pressKeyRect)#.blit is just drawing this out using the given perameters
#This function is responcible for prompting the user to press a key to continue and is triggered on the start menu to begin the game, and when the player looses to restart.

def checkForKeyPress():
  if len(pygame.event.get(QUIT)) > 0: #This statement checks if the player wants to quit by checking the events if this is true the terminate() function will close the window
    terminate()

  keyUpEvents = pygame.event.get(KEYUP)#this is all the keys
  if len(keyUpEvents) == 0:#checks if any key that wasn't an terminate key is pressed and then will restart the game
    return None
  if keyUpEvents[0].key == K_ESCAPE: #if the escape key is hit it will also terminate the window
    terminate()
  return keyUpEvents[0].key

#Checks if a key has been pressed and based on that key will perform the respected action

#AKSHAT REGANI END

#ROBERT MIRANDA START


#creates the start screen that opens when the user first runs the code
def showStartScreen():
  #sets the font and size of the letters (100 points in size)
  titleFont = pygame.font.Font('freesansbold.ttf', 100)

  #renders the word "Wormy!" in the font set above and makes the text white with a green background
  titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)

  #renders the word "Wormy!" again with the font set above but in green text with a transparent background this time
  titleSurf2 = titleFont.render('Wormy!', True, GREEN)

  degrees1 = 0
  degrees2 = 0
  showmenu = False
  #causes the words on the start scren to rotate
  while showmenu == False:
    DISPLAYSURF.fill(BGCOLOR)  #sets the display to black
    rotatedSurf1 = pygame.transform.rotate(
      titleSurf1, degrees1
    )  # creates a new surface object containing the word "Wormy!" (the one with the background) that is rotated by degrees1 degrees
    rotatedRect1 = rotatedSurf1.get_rect(
    )  #creates a new rectangle around the rotated surface object
    rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2
                           )  #gets the center of the rectangle
    DISPLAYSURF.blit(rotatedSurf1,
                     rotatedRect1)  #displays the new surface object

    rotatedSurf2 = pygame.transform.rotate(
      titleSurf2, degrees2
    )  #creates a new surface object containing the word "Wormy!" (the one without the background) that is rotated by degrees2 degrees
    rotatedRect2 = rotatedSurf2.get_rect(
    )  #creates a new rectangle around the rotated surface object
    rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2
                           )  #gets the center of the rectangle
    DISPLAYSURF.blit(rotatedSurf2,
                     rotatedRect2)  #displays the new surface object

    drawPressKeyMsg()  #tells the user to press a button to start the game
    
    if checkForKeyPress():  #checks if the user pressed a key
      showmenu = True

    #   replace this return statement with the design of our menu
    #   we want two buttons and one button (regular mode) returns one value the other button (our changed mode) returns another value
    #   then in the main function instead of running the game as soon as this function is broken out of, it would check which value is returned and run a different version of the game depending on what the value is
    
    pygame.display.update()  #updates the display
    FPSCLOCK.tick(FPS)  #sets the frame rate
    degrees1 += 3  # rotate by 3 degrees each frame
    degrees2 += 7  # rotate by 7 degrees each frame

def drawMenuButtons():
      pygame.event.get()  # clear event queue
      DISPLAYSURF.fill(BGCOLOR)
      btn_colour = (100,100,100) #Button colour 
      txt_colour = (250, 200, 200) #Text colour

      pygame.draw.rect(DISPLAYSURF,btn_colour,[ 100, 200,150,50])
      normaltxt = BASICFONT.render("Normal", True, txt_colour)      
      DISPLAYSURF.blit(normaltxt, (145, 215))
      
      
      pygame.draw.rect(DISPLAYSURF,btn_colour,[ 400, 200,150,50])
      hardtxt = BASICFONT.render("Hard", True, txt_colour)      
      DISPLAYSURF.blit(hardtxt, (445, 215))
      pygame.display.update()
      FPSCLOCK.tick(FPS)  
      button_press = False

      while button_press == False:
        for event in pygame.event.get():
          if event.type == QUIT:
            terminate()

          elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 100 <= mouse [0] <= 250  and  200 <= mouse[1] <= 250:
              print("normal mode selected!")
              button_press = True
              return ("normal")

            elif 400<= mouse[0] <= 550 and 200 <= mouse[1] <= 250:
              print("hard mode selected!")
              button_press = True
              return ("hard")
          

def terminate():  #shuts down the game
  pygame.quit()  #exits pygame
  sys.exit()  #exits from python


def getRandomLocation():  #used to decide where the apple appears
  return {
    'x': random.randint(0, CELLWIDTH - 1),  #returns a random x coordinate
    'y': random.randint(0, CELLHEIGHT - 1)  #returns a random y coordinate
  }


def showGameOverScreen(
):  #prints the game over screen on the display when the user loses
  gameOverFont = pygame.font.Font('freesansbold.ttf', 150)  #sets the font
  gameSurf = gameOverFont.render(
    'Game', True, WHITE)  #renders the word "game" in the above font
  overSurf = gameOverFont.render(
    'Over', True, WHITE)  #renders the word "over" in the above font
  gameRect = gameSurf.get_rect()  #creates a rectangle around the word "game"
  overRect = overSurf.get_rect()  #creates a rectangle around the word "over"
  gameRect.midtop = (
    WINDOWWIDTH / 2, 10
  )  #moves the rectangle containting the word "game" to the top center of the display
  overRect.midtop = (
    WINDOWWIDTH / 2, gameRect.height + 10 + 25
  )  #moves the rectangle containting the word "over" to the top center of the display

  DISPLAYSURF.blit(
    gameSurf, gameRect
  )  #displays the word "game" and the rectangle around it (the rectangel is transparent)
  DISPLAYSURF.blit(
    overSurf, overRect
  )  #displays the word "over" and the rectangle around it (the rectangel is transparent)
  drawPressKeyMsg()  #tells the user to press a button to start the game
  pygame.display.update()  #updates the display
  pygame.time.wait(500)  #pauses for 500 milliseconds
  checkForKeyPress()  # clear out any key presses in the event queue

  while True:
    if checkForKeyPress():  #checks if the user pressed a key to start the game
      pygame.event.get()  # clear event queue
      return


#ROBERT MIRANDA END


#AKSHAT REGANI START
def drawScore(score):
  scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE) #Is the Image of the Score: text with (score) holding the value
  scoreRect = scoreSurf.get_rect() #Draws a rectangle on the entire surface
  scoreRect.topleft = (WINDOWWIDTH - 120, 10) #Will display this box with those dimensions 120x10
  DISPLAYSURF.blit(scoreSurf, scoreRect) #Displays the image with the score and rectangle

def getRandomColour(colourScore):
    colourNum = random.randint(1,7)

    #Dark outside Light Inside
    if(colourScore % 5 == 0):
        if colourNum == 1:
            outside = DARKORANGE
            inside = ORANGE
        if colourNum == 2:
            outside = DARKGREEN
            inside = GREEN
        if colourNum == 3:
            outside = DARKYELLOW
            inside = YELLOW
        if colourNum == 4:
            outside = DARKCYAN
            inside = CYAN
        if colourNum == 5:
            outside = DARKBLUE
            inside = BLUE
        if colourNum == 6:
            outside = DARKPINK
            inside = PINK
        if colourNum == 7:
            outside = RED
            inside = LIGHTRED
    else:
      outside = DARKGREEN
      inside = GREEN
    return [outside, inside]

def drawWorm(wormCoords):#Takes the coordinates and then will draw the worm accordingly
  for coord in wormCoords:
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    #These two will hold the coordinates for the x and y postion 
    Fcolour = getRandomColour(len(wormCoords) - 3)
    wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) #Stores the data of the worm segment on its respceted coordinate and cell
    pygame.draw.rect(DISPLAYSURF, Fcolour[0], wormSegmentRect)#Draws the worm out line of the worm
    wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, #this is a modified version of wormSegmentRect since "The inner bright green rectangle starts 4 pixels to the right and 4 pixels below the topleft corner of the cell. The width and height of this rectangle are 8 pixels less than the cell size, so there will be a 4 pixel margin on the right and bottom sides as well." As said in documentation
                                       CELLSIZE - 8)
    pygame.draw.rect(DISPLAYSURF, Fcolour[1], wormInnerSegmentRect)#Draws the inner green of the worm

    #(THE WORM SEGMENT IS A BOX WITH THE OUTER PORTION DARKGREEN AND THE INNER LIGHT GREEN)


def drawApple(coord): #spawns the apple
  x = coord['x'] * CELLSIZE
  y = coord['y'] * CELLSIZE
  #These two will hold the coordinates for the x and y postion 
  appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
  #This tells the function bellow which cell to draw said rectangle
  pygame.draw.rect(DISPLAYSURF, RED, appleRect) #pygame.draw will draw the apple using the colour, the rectangle size (cell)


def drawGrid(): #Is responcible for drawing out the grid the snake moves along
  for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
    pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))#this function will draw the vertical lines
  for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
    pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))#this function will draw the horizontal lines


if __name__ == '__main__':
  main()
#Once the functions and constants and global variables have been defined and created the main() function is the one that starts the game
  
#AKSHAT REGANI END
