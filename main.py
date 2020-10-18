import sys
import pygame
import random
import math
from Tile import *
from Grid import *

#basic parameters
"colors"
Black = (0,0, 0)
White = (255, 255, 255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
yellow = (204,204,0)
#flag_image = pygame.image.load('flag.png')   #ADD FLAG IMAGE
#bomb_image = 

MARGIN = 10
TILESIZE = 50
X_SCREEN_OFFSET = 0
Y_SCREEN_OFFSET = 200

def click_square():
	"""
	Open clicked square
	"""
	# NOTE: first square clicked is never a bomb and neither will its neighbors
	pass

def isLose():
	"""
	Checks if bomb is clicked (you ded)
	"""
	pass 

def isWin() -> bool:
	"""
	Return True if all non-bomb squares are opened
	"""
	# NOTE: incorrectly marked bombs prevent win
	pass


def bomb_status():
	"""
	Show number of bombs left
	
	"""

	pass

def timer():
	"""
	Timer (max 999 seconds)
	"""
	
	pass

def reset():
  pass

#seting up the Mines 

#Uses pygame to create a graphic board
def drawBoard(screen, gameBoard):
  for i in range(gameBoard.height):
    for j in range(gameBoard.width):
      x = (X_SCREEN_OFFSET + MARGIN) + i * (TILESIZE + MARGIN)
      y = (Y_SCREEN_OFFSET + MARGIN) + j * (TILESIZE + MARGIN)
      gameBoard.getTile(i,j).setOriginX(x)
      gameBoard.getTile(i,j).setOriginY(y)
      pygame.draw.rect(screen, White, (x,y,TILESIZE,TILESIZE))

def openTile(screen, gameBoard, tile):
  posX = tile.getOriginX()
  posY = tile.getOriginY()

  print("opening tile ", tile.getX(), tile.getY())

  pygame.draw.rect(screen, Red, (posX,posY,TILESIZE,TILESIZE))

  if tile.reveal() == -1:
    font = pygame.font.SysFont(None, 60)
    img = font.render('X', True, Black)
    screen.blit(img, (posX+5, posY+5))
    return screen
  else:
    font = pygame.font.SysFont(None, 60)
    img = font.render(str(tile.getBombsNearby()), True, Black)
    screen.blit(img, (posX+5, posY+5))
    if tile.reveal() == 0:
      neighbors = gameBoard.getNeighbors(tile)
      for thisTile in neighbors:
        if not (thisTile.hasBeenSeen() or thisTile.reveal() == -1):
          return openTile(screen, gameBoard, thisTile)

  #end else
  

def run_game():

  # Initialize game and create a screen object.
  pygame.init()
  pygame.font.init()
  screen = pygame.display.set_mode((800, 800))
  pygame.display.set_caption("Minesweeper")
  # Start the main loop for the game.
  
  screen.fill(Black)

  gameBoard = Grid(1)
  drawBoard(screen, gameBoard)
  
      
  # TODO: instead of just drawing new rectangle, draw bomb/empty/nearbyBombs
  while True:
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        print(pos)
        #Pygame normally has 0,0 as the coords for top left, for some reason
        #here it sets it to 0,200. X and Y_SCREEN_OFFSET accounts for that
        posX = (pos[0] - (X_SCREEN_OFFSET + MARGIN)) // (TILESIZE + MARGIN) 
        posY = (pos[1] - (Y_SCREEN_OFFSET + MARGIN)) // (TILESIZE + MARGIN)
        print("posX = ", posX)
        print("posY = ", posY)
        
        #if tile is valid index
        if posX < gameBoard.width and posY < gameBoard.height:
          tile = gameBoard.getTile(posX, posY)
          openTile(screen, gameBoard, tile)
      
      pygame.display.flip()
    #end forevent loop
  #end while loop
#end run_game


run_game()