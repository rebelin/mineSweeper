import sys
import pygame
import random
import math
from Tile import *
from Grid import *
import time

#basic parameters
MARGIN = 10
TILESIZE = 50
X_SCREEN_OFFSET = 0
Y_SCREEN_OFFSET = 200
tilesVisited = 0
alive = True
difficulty = 1
bombsFlagged = 0
numMines = 0


"colors"
Black = (0,0, 0)
White = (255, 255, 255)

DarkGrey = (100,100,100)
LightGrey = (200,200,200)

Red = (218,63,45)
Green = (53,169,69)
Blue = (65,103,205)
Yellow = (204,204,0)
colors = [Blue, Green, Red, Yellow]
flag_image = pygame.image.load('images/flag.png')
flag_image = pygame.transform.scale(flag_image, (TILESIZE, TILESIZE))
bomb_image = pygame.image.load('images/bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (TILESIZE, TILESIZE))

#Logo source: https://www.facebook.com/minesweepergo/
logo = pygame.image.load('images/logo.jpeg')
gameover = pygame.image.load('images/gameover.jpg')
win = pygame.image.load('images/win.jpg')


def openTile(screen, gameBoard, tile):
  global alive
  global tilesVisited 
  global bombsFlagged

  if tile.hasFlag():
    return
  if not tile.hasBeenSeen():
    tilesVisited += 1
    print("tilesVisited: ", tilesVisited)
  
  posX = tile.getOriginX()
  posY = tile.getOriginY()

  print("opening tile ", tile.getX(), tile.getY())

  pygame.draw.rect(screen, LightGrey, (posX,posY,TILESIZE,TILESIZE))

  outcome = tile.reveal()

  if outcome == -1: #Bomb
    global alive
    screen.blit(bomb_image, (posX, posY))
    alive = False
    return
  else: #Empty or Numbered
    font = pygame.font.SysFont(None, 60)
    nearby_bombs = tile.getBombsNearby()
    if nearby_bombs > 0: #Only put num if > 0
      color = nearby_bombs % len(colors)
      img = font.render(str(tile.getBombsNearby()), True, colors[color-1])
      screen.blit(img, (posX+5, posY+5))
      neighbors = gameBoard.getNeighbors(tile)

    if outcome == 0: 
      neighbors = gameBoard.getNeighbors(tile)
      for thisTile in neighbors:
        if not (thisTile.hasBeenSeen()):
          openTile(screen, gameBoard, thisTile)
  #end else
  


def drawTitle(screen):
  screen.blit(logo, (100, 300))
  text1 = font.render('Easy', True, Black, LightGrey)
  textRect1 = text1.get_rect()  
  textRect1.center = (100, 600)
  screen.blit(text1, textRect1) 
  text2 = font.render('Medium', True, Black, LightGrey)
  textRect2 = text2.get_rect()  
  textRect2.center = (260, 600)
  screen.blit(text2, textRect2) 
  text3 = font.render('Hard', True, Black, LightGrey)
  textRect3 = text3.get_rect()  
  textRect3.center = (425, 600)
  screen.blit(text3, textRect3) 

#Uses pygame to create a graphic board
def drawBoard(screen, gameBoard):
  for i in range(gameBoard.height):
    for j in range(gameBoard.width):
      x = (X_SCREEN_OFFSET + MARGIN) + i * (TILESIZE + MARGIN)
      y = (Y_SCREEN_OFFSET + MARGIN) + j * (TILESIZE + MARGIN)
      gameBoard.getTile(i,j).setOriginX(x)
      gameBoard.getTile(i,j).setOriginY(y)
      pygame.draw.rect(screen, DarkGrey, (x,y,TILESIZE,TILESIZE))

def drawEndgame(screen):
  global bombsFlagged
  global numMines
  screen.fill(Black)
  screen.blit(gameover, (100, 300))
  text = "Bombs Found: " + str(bombsFlagged) + " | Bombs Left: " + str(numMines-bombsFlagged)
  stat = font.render(text, True, Black, LightGrey)
  statRect = stat.get_rect()  
  statRect.center = (350, 600)
  screen.blit(stat, statRect)

def drawWingame(screen):
  screen.fill(Black)
  screen.blit(win, (100, 300))
  stat = font.render("You found or flagged all the mines!", True, Black, LightGrey)
  statRect = stat.get_rect()  
  statRect.center = (350, 600)
  screen.blit(stat, statRect)




pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32) 
def run_game():
  global alive
  global difficulty
  global tilesVisited
  global numMines
  global bombsFlagged

  if difficulty == 1:
    numTiles = 64
    numMines = 10
    numFlags = 10
  elif difficulty == 2:
    numTiles = 256
    numMines = 40
    numFlags = 40
  elif difficulty == 3:
    numTiles = 480
    numMines = 99
    numFlags = 99

  #width = TILESIZE * ((numMines + TILESIZE) // MARGIN)
  #height = TILESIZE * ((numMines + TILESIZE) // MARGIN)
  tilesVisited = 0


  # Initialize game and create a screen object.
  pygame.init()
  pygame.font.init()
  screen = pygame.display.set_mode((800, 800))
  pygame.display.set_caption("Minesweeper")
  # Start the main loop for the game.
  
  screen.fill(Black)

  drawTitle(screen)
  pygame.display.flip()
  pygame.event.clear()
  while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.MOUSEBUTTONUP:
      if pygame.mouse.get_pos()[0] < 200:
        difficulty = 1
      elif pygame.mouse.get_pos()[0] < 350:
        difficulty = 2
      else:
        difficulty = 3
      screen.fill(Black)
      break
  
  

  gameBoard = Grid(difficulty)
  drawBoard(screen, gameBoard)
  
  while alive and tilesVisited+numMines < numTiles:
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.MOUSEBUTTONUP:
        print("alive in main loop:", alive)
        pos = pygame.mouse.get_pos()
        print(pos)
        #Pygame normally has 0,0 as the coords for top left, for some reason
        #here it sets it to 0,200. X and Y_SCREEN_OFFSET accounts for that
        indexX = (pos[0] - (X_SCREEN_OFFSET + MARGIN)) // (TILESIZE + MARGIN) 
        indexY = (pos[1] - (Y_SCREEN_OFFSET + MARGIN)) // (TILESIZE + MARGIN)
        print("indexX = ", indexX)
        print("indexY = ", indexY)
        
        #if tile is valid index
        if indexX < gameBoard.width and indexY < gameBoard.height:
          tile = gameBoard.getTile(indexX, indexY)
          print("ButtonClicked: ", event.button)
          if event.button == 1: #left click
            openTile(screen, gameBoard, tile)
          elif event.button == 3 and not tile.hasBeenSeen(): #right click
            tileX = tile.getOriginX()
            tileY = tile.getOriginY()

            if tile.hasFlag():
              tile.setFlag(False)
              if tile.hasBomb:
                bombsFlagged -= 1
              pygame.draw.rect(screen, DarkGrey, (tileX,tileY,TILESIZE,TILESIZE))
              print("deflagged")
            else:
              tile.setFlag(True)
              if tile.hasBomb:
                bombsFlagged += 1
              screen.blit(flag_image, (tileX, tileY))
              print("flagged")
      
      pygame.display.flip()
    #end forevent loop
  #end while loop


  time.sleep(3)

  if (tilesVisited+numMines) == numTiles:
    print("YOU WIN")
    drawWingame(screen)
    pygame.display.flip()
    pygame.event.clear()
    while True:
      event = pygame.event.wait()
      if event.type == pygame.QUIT:
        pygame.quit()
      elif event.type == pygame.MOUSEBUTTONUP:
        screen.fill(Black)
        break
  else:
    drawEndgame(screen)
    pygame.display.flip()
    pygame.event.clear()
  while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.MOUSEBUTTONUP:
      screen.fill(Black)
      break

#end run_game


run_game()

