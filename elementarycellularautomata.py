import numpy as np      # import NumPy
import time             # import Time
import pygame as pg     # import PyGame
import math             # import Math
pg.font.init()          # Initialize font module from pygame

width = 1433.6; height = 1008                  # Establish width and height of the grid
bg = (35, 35, 35)                           # Establish background color of window
border = 1; color = (200, 200, 200)         # Establish color and border size of cells
font = pg.font.SysFont(None, int(height/18))
font2 = pg.font.SysFont(None, int(height/20))
text_rule = font.render("Rule",1,color)
cells = 255; lines = cells           # Establish number of cell in each dimension
celw = width / cells; celh = width / lines    # Establish the width and height of a cell depending on the size of the window and the number of cells
extra = 200
pause = 1                                   # Establish the boolean variable pause, which is used to determine whether the game is paused or not
kill = 0                                    # Declare the kill boolean variable, if set to TRUE, the program will end                                      # Declare i as the number of iterations of the game

screen = pg.display.set_mode([int(width + (width/8)),height])                           # Set up the display with size defined by width and height of the grid, plus the border so when cells are drawn it does not get cut off the edges and plus a fourth of the width to display text
pg.display.set_caption("Elementary Cellular Automaton")   # Set up the window title and icon

def newline(y):
    for x in range(1,cells+(2*extra)-1):
        poly = [(round((x-extra)*celw         ), round((y)*celh        )),                # This list of points contains the ordered vertices of a square, which will define the shape of the cell.
                (round((x-extra)*celw + celw  ), round((y)*celh        )),                # Each vertex is calculated multiplying the cell coordinate with the cell width or height
                (round((x-extra)*celw + celw  ), round((y)*celh + celh )),                # and then adding the height or the width depending on the vertex
                (round((x-extra)*celw         ), round((y)*celh + celh ))]
        if not pause:                                                           # If the game is paused, the operations for updating the game will not happen, and the gameState will not change
            if not y == 0:
                nvalue = (str(gameState[(x-1)])+str(gameState[x])+str(gameState[(x+1)]))  # To know how many living neighbours a cell has, we sum the value of the 8 cells surrounding the cell (excluding it) in the matrix, if the cell is in the edge, the modulus operation will output the cell on the other side, behaving like a torus. For example, in (5,74), if there are 75 cells and it begins counting with 0, when checking for (5,75), it will check for (5,0).
                newgameState[x] = rulesetbin[7-int(nvalue, 2)]
            if not poly[2][0] > width and not poly[0][0] < 0 or poly[0][1] > int((height/20)*3.5):
 
                if int(newgameState[x]) == 1:pg.draw.polygon(screen, color, poly, 0)
    pg.display.update()

for i in range(0,256):
    if kill: break
    gameState = [0] * int(((cells-1)/2)+extra)  + [1] + [0] * int(((cells-1)/2)+extra)     # Establishing the matrix gameState which contains the values of all cells, its dimensions are defined with the number of cells
    y = 0
    text_i = font.render(str(i),1,color)
    rulesetbin = format(i,'#010b')
    rulesetbin = rulesetbin.replace("0b", "")
    text_bin = font2.render(rulesetbin,1,color)
    print(rulesetbin)
    screen.fill(bg)                                                                                         # Coloring the background with the colour established in bg
    screen.blit(text_rule, (width + border + int(width/16) - text_rule.get_width() // 2, int((height/20)*1) - text_rule.get_height() // 2))
    screen.blit(text_i, (width + border + int(width/16) - text_i.get_width() // 2, int((height/20)*2) - text_i.get_height() // 2))
    screen.blit(text_bin, (width + border + int(width/16) - text_bin.get_width() // 2, int((height/20)*3) - text_bin.get_height() // 2))
    while 1:                                                                            # Main loop of the game, if it ends (and the only way is through a break statement), the game ends
        for event in pg.event.get():                                                    # Check for every event recorded by pygame
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: pause = not pause  # If the space bar is pressed, the value of game changes, pausing or unpausing the game
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: kill = 1          # If the ESC key is pressed, the value if kill changes to TRUE
        if kill: break
        if not pause:
            newgameState = [0]*(cells+(2*extra)) # If kill is TRUE, the while loop breaks and the program ends                                              # We make a copy of the game matrix in which we are going to make the changes each generation so we do not overwrite gameState while we are reading it
        if y == 0:
            newgameState = gameState
        if not pause:
            newline(y)
            y += 1
            if (y)*celh + celh > height:
                break
        if not y == 0:
            gameState = newgameState
    time.sleep(0.25)
