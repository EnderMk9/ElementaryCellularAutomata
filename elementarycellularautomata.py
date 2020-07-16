import numpy as np      # import NumPy
import pygame as pg     # import PyGame
pg.font.init()          # Initialize font module from PyGame

textsetup = 0   # variable that records if the initialization of the text on screen has finished
varsetup = 0    # variable that records if the initialization of the variables has finished
setup = 0       # variable that records if the initial setup has concluded

while not varsetup:     # Setup of variables and text
    width = 1401; height = 979                   # Establish width and height of the grid, the default ones result in a 1776x999 window
    #width = 1516; height = 1060                 # This values result in a 1920x1080 window
    bg = (200, 200, 200); color = (50, 50, 50)   # Establish background color of window and color for text and the cell grid
    margin = 10; extra = 1                       # Establish border size of cells and margin of the grid and the extra cell at the side which are not visualized
    tlines = 250; celh = height / tlines         # Establish an arbitrary number for the total number of lines and establish the height of those lines dividing the height of the grid by the number of lines
    celw = celh; celX = round(width/celw)        # Establish that the width of a cell is equal to it's height, making it a square, a with that width, calculate the number of rows that fit in the grid
    kill = 0; ftop = 0; rulemode = 0; turbo = 0; pauset = 0 # Establish certain variables that will keep track if certain modes or events in the programme are activated
    #frame = 0; record = 1                       # Establish certain optional variables for the recording mode
    rule = 30                                    # Establish the default rule of the automaton
    while not textsetup:    # Setup text
        font = pg.font.SysFont(None, int(height/18))                    # We set up font 1 for texts, its size depends on the height of the gird. BIG
        font2 = pg.font.SysFont(None, int(height/25))                   # We set up font 2 for texts, its size depends on the height of the gird. MEDIUM
        font3 = pg.font.SysFont(None, int(height/40))                   # We set up font 3 for texts, its size depends on the height of the gird. SMALL
        text_elem = font.render("Elementary",1,color)                   # TEXT FOR "Elementary"           color "color"   antialias = 1
        text_cel = font.render("Cellular",1,color)                      # TEXT FOR "Cellular"             color "color"   antialias = 1
        text_auto = font.render("Automata",1,color)                     # TEXT FOR "Automata"             color "color"   antialias = 1
        text_rule = font.render("Rule:", 1, color)                      # TEXT FOR "Rule:"                color "color"   antialias = 1
        text_paused = font.render("Paused",1,color)                     # TEXT FOR "Paused"               color "color"   antialias = 1
        text_running = font.render("Running",1,color)                   # TEXT FOR "Running"              color "color"   antialias = 1
        text_ln = font.render("Line:",1,color)                          # TEXT FOR "Line"                 color "color"   antialias = 1
        text_ins1 = font3.render("LClick - Turn alive",1,color)         # TEXT FOR Instruc1               color "color"   antialias = 1
        text_ins2 = font3.render("RClick - Kill cell",1,color)          # TEXT FOR Instruc2               color "color"   antialias = 1
        text_ins3 = font3.render("SPACE - Pause/Unpause",1,color)       # TEXT FOR Instruc3               color "color"   antialias = 1
        text_ins4 = font3.render("W - Increase lines",1,color)  # TEXT FOR Instruc4               color "color"   antialias = 1
        text_ins5 = font3.render("S - Decrease lines",1,color)  # TEXT FOR Instruc5               color "color"   antialias = 1
        text_ins6 = font3.render("BACKSPACE - Reset",1,color)           # TEXT FOR Instruc6               color "color"   antialias = 1
        text_ins7 = font3.render("F/G - Previous/Next rule", 1, color)  # TEXT FOR Instruc7               color "color"   antialias = 1
        text_ins8 = font3.render("T - FromTop act.",1,color)            # TEXT FOR Instruc8               color "color"   antialias = 1
        text_ins9 = font3.render("R - RuleView act.", 1, color)         # TEXT FOR Instruc9               color "color"   antialias = 1
        text_ins0 = font3.render("B - Turbo act.", 1, color)            # TEXT FOR Instruc0               color "color"   antialias = 1
        text_insa = font3.render("ESC - End Game", 1, color)            # TEXT FOR Instruca               color "color"   antialias = 1
        textsetup = 1       # Finish text setup
    varsetup = 1            # Finish variable and text setup

def setrule(ruleset):       # Function which converts the rule passed as an argument to binary so we can use it
    global rulesetbin       # Set this variable as global
    rulesetbin = format(ruleset, '#010b').replace("0b", "")       # Convert to an 8 digit binary and remove the prefix 0b

def reset():        # Function which resets the state of the game
    global gameState, newgameState, rulesetbin,pause,line,ftop      # Set these variables as global
    gameState = np.zeros((celX+2*extra,tlines))                     # Establishing the matrix gameState which contains the values of all cells, its dimensions are defined with the number of lines and rows
    if not ftop: gameState[(celX+2*extra)//2,tlines-1] = 1          # If the normal mode, from the bottom, is activated, we set the cell in the middle of the last line as alive
    elif ftop: gameState[(celX+2*extra)//2,0] = 1                   # If FromTop mode is enables, it instead places the living cell in the first line
    newgameState = np.zeros((celX+2*extra,tlines))                  # Declaring the matrix newgameState in which we're going to write the changes before writing them into gameState again
    pause = 1; line = 0                                             # Set the game as paused and reset the line count

def evolve():    # Function to update the value of cells acording to the rules of the ECA. Default mode, scroll from bottom
    global it,line,rulesetbin,gameState,newgameState,celX,tlines    # Set these variables as global
    newgameState = np.zeros((celX+2*extra,tlines))                  # Clean the newgameState matrix
    for y in range(0,line+1):                                       # Check for only the lines that have already been calculated plus 1
        for x in range(0,celX+2*extra):                             # Check for all the rows
            nvalue = (str(int(gameState[(x-1)%(celX+2*extra),(tlines-1-y)%tlines]))+str(int(gameState[x,(tlines-1-y)%tlines]))+str(int(gameState[(x+1)%(celX+2*extra),(tlines-1-y)%tlines])))  # We store the values of the cell and the two adyacent cells in a string
            if not y == tlines-1: newgameState[x,(tlines-2-y)%tlines] = gameState[x,(tlines-1-y)%tlines]        # Saves the current state of the line to the superior line on the matrix, except if it is the last line, the one on top.
            newgameState[x,(tlines-1-y)%tlines] = rulesetbin[7 - int(nvalue, 2)]        # Saves the value of the next iteration in the same line, to calculate this value, we convert the nheight to an int which will act as the reverse index of the number on the binary string of the ruleset to set that iteration
    line += 1                 # When we have finished calculating the iteration, we add one to the number of lines calculated
    gameState = newgameState  # save the changes made in newgameState to gameState

def evolveftop():    # Function to update the value of cells acording to the rules of the ECA. FromTop mode
    global it,line,rulesetbin,gameState,newgameState,celX,tlines # set these variables as global
    newgameState = np.copy(gameState)       # Make newgameState a copy of gameState because we will not be updating previous lines, just one line at a time, defined by line
    for x in range(0,celX+2*extra):         # For every row in the matrix
        nvalue = (str(int(gameState[(x-1)%(celX+2*extra),(line)%tlines]))+str(int(gameState[x,(line)%tlines]))+str(int(gameState[(x+1)%(celX+2*extra),(line)%tlines])))  # We store the values of the cell and the two adyacent cells in a string
        newgameState[x,(line+1)%tlines] = rulesetbin[7 - int(nvalue, 2)]        # Saves the value of the next iteration in the next line, to calculate this value, we convert the nheight to an int which will act as the reverse index of the number on the binary string of the ruleset to set that iteration
    line += 1                 # When we have finished calculating the iteration, we add one to the number of lines calculated
    gameState = newgameState  # save the changes made in newgameState to gameState

def drawmatrix():       # Function to update and draw the cells according to the matrix
    global celw,margin,celh,celX,tlines,screen,gameState,extra      # Set these variables as global
    for x in range(0,celX):                                         # Two for loops x and y for the number of cells in each dimension, x and y are the coordinates of the cells
        for y in range(0, tlines):
            if not gameState[x+extra,y] == 0:                       # Only do the next calculations if the cell is alive
                poly = [(round(x*celw        + margin), round(y*celh        + margin)), # This list of points contains the ordered vertices of a square, which will define the shape of the cell.
                        (round(x*celw + celw + margin), round(y*celh        + margin)), # Each vertex is calculated multiplying the cell coordinate with the cell width or height
                        (round(x*celw + celw + margin), round(y*celh + celh + margin)), # and then adding the height or the width depending on the vertex
                        (round(x*celw        + margin), round(y*celh + celh + margin))]
                pg.draw.polygon(screen, ((x/celX)*125 +50,(y/tlines)*125 + 50,((((celX+1)/(x+1))+((tlines+1)/(y+1)))/(celX+tlines))*75 +100 ), poly, 0)  # DRAW The square will be filled (border = 0) with a color which depends on the grid coordinate of the cell

def updategrid():   # Function to update and draw the grid
    global celX,tlines,celw,celh,pause,gameState,newgameState,color,screen,line,ftop,rule,pauset    # Set these variables as global
    if not pause:                       # If the game is paused, the gameState will not be updated
        if not ftop: evolve()           # If ftop is not activated, update the matrix using the normal mode
        elif ftop: evolveftop()         # If ftop is activated, update the matrix using ftop mode
    pg.draw.polygon(screen,color,[(margin,margin),(int(celX*celw)+margin,margin),(int(celX*celw)+margin,int(tlines*celh)+margin),(margin,int(tlines*celh)+margin)],0)       # Draw the complete grid screen
    drawmatrix()                        # Draw the living cells in the grid
    pg.display.flip()                   # update all the changes on the screen
    if rulemode and line >= tlines:     # If RuleView mode is activated and we have reached the last line:
        if not turbo and not pauset: pause = 1; pauset = 1      # If turbo is not activated, it will pause, unless it had already been paused for the same reason
        elif turbo or not pause:                                # If turbo is activated or we have unpaused:
            reset(); rule +=1; setrule(rule)                    # Reset the state of the game, increase one the rule and update it
            pause = 0; pauset = 0                               # Unpause the game and the pauset set to 0 so if turbo is not activated, it will pause when it finishes

def update_text(): # Function to update the text on screen
    global celX,line,rulesetbin,text_rul,text_x
    text_i = font2.render(str(line),1,color)                            # TEXT FOR number of iterations         color "color"   antialias = 1
    text_dim = font.render(str(celX) + " x " + str(tlines),1,color)     # TEXT FOR dimension of the grid        color "color"   antialias = 1
    text_rul = font2.render(str(rule) + " - Bin: " + rulesetbin,1,color)# TEXT FOR rule                         color "color"   antialias = 1
    text_ftop = font2.render("From Top Mode",1,color)                   # TEXT FOR ftop                         color "color"   antialias = 1
    text_rmode = font2.render("RuleView Mode ",1,color)                 # TEXT FOR rmode                        color "color"   antialias = 1
    text_turbo = font2.render("Turbo Mode",1,color)                     # TEXT FOR turbo                        color "color"   antialias = 1
    text_x = int(width + margin*1.5 + int((width+2*margin)/8))          # Define the x coordinate for the texts
    screen.blit(text_elem,  (text_x - text_elem.get_width() // 2,  int(height/20)*1      + margin - text_elem.get_height() // 2))
    screen.blit(text_cel,   (text_x - text_cel.get_width() // 2,   int(height/20)*2      + margin - text_cel.get_height() // 2))
    screen.blit(text_auto,  (text_x - text_auto.get_width() // 2,  int(height/20)*3      + margin - text_auto.get_height() // 2))
    screen.blit(text_dim,   (text_x - text_dim.get_width() // 2,   int((height/20)*5.5)  + margin - text_dim.get_height() // 2))
    screen.blit(text_rule,  (text_x - text_rule.get_width() // 2,  int(height/20)*7      + margin - text_rule.get_height() // 2))
    screen.blit(text_rul,   (text_x - text_rul.get_width() // 2,   int(height/20)*8      + margin - text_rul.get_height() // 2))
    screen.blit(text_ln,    (text_x - text_ln.get_width() // 2,    int((height/20)*9.5)  + margin - text_ln.get_height() // 2))
    screen.blit(text_i,     (text_x - text_i.get_width() // 2,     int((height/20)*10.5) + margin - text_i.get_height() // 2))
    if ftop:     screen.blit(text_ftop,  (text_x - text_ftop.get_width() // 2,  int((height/20)*11.5)   + margin - text_ftop.get_height() // 2))    # Only display if ftop is active
    if rulemode: screen.blit(text_rmode, (text_x - text_rmode.get_width() // 2, int((height/20)*12.5)   + margin - text_rmode.get_height() // 2))   # Only display if RuleViewMode is active
    if turbo:    screen.blit(text_turbo, (text_x - text_turbo.get_width() // 2, int((height/20)*13.5)   + margin - text_turbo.get_height() // 2))   # Only display if Turbo is active
    screen.blit(text_ins1,  (text_x - text_ins1.get_width() // 2,  int((height/20)*14.5)   + margin - text_ins1.get_height() // 2))
    screen.blit(text_ins2,  (text_x - text_ins2.get_width() // 2,  int((height/20)*15) + margin - text_ins2.get_height() // 2))
    screen.blit(text_ins3,  (text_x - text_ins3.get_width() // 2,  int((height/20)*15.5)   + margin - text_ins3.get_height() // 2))
    screen.blit(text_ins4,  (text_x - text_ins4.get_width() // 2,  int((height/20)*16) + margin - text_ins4.get_height() // 2))
    screen.blit(text_ins5,  (text_x - text_ins5.get_width() // 2,  int((height/20)*16.5)   + margin - text_ins5.get_height() // 2))
    screen.blit(text_ins6,  (text_x - text_ins6.get_width() // 2,  int((height/20)*17) + margin - text_ins6.get_height() // 2))
    screen.blit(text_ins7,  (text_x - text_ins7.get_width() // 2,  int((height/20)*17.5)   + margin - text_ins7.get_height() // 2))
    screen.blit(text_ins8,  (text_x - text_ins8.get_width() // 2,  int((height/20)*18)   + margin - text_ins8.get_height() // 2))
    screen.blit(text_ins9,  (text_x - text_ins9.get_width() // 2,  int((height/20)*18.5)   + margin - text_ins9.get_height() // 2))
    screen.blit(text_ins0,  (text_x - text_ins0.get_width() // 2,  int((height/20)*19)   + margin - text_ins0.get_height() // 2))
    screen.blit(text_insa,  (text_x - text_insa.get_width() // 2,  int((height/20)*19.5)   + margin - text_insa.get_height() // 2))
    # screen.blit render all the different texts in a relative centered position position to the right of the grid

def update_title_run():     # Function to update the title and the information in it
    global celX,tlines,rule,rulesetbin,line
    if not pause:                                                                   # Checks if the game is not paused
        pg.display.set_caption("Cellular Elementary Automata - " + str(celX) + "x" + str(tlines) + " - Rule: " + str(rule) + " - " + rulesetbin + " - RUNNING - " + "{ft}".format(ft="FromTop - " if ftop else "") + "{rv}".format(rv="RuleView - " if rulemode else "") + "{tb}".format(tb="Turbo - " if turbo else "") + "LINE " + str(line))  # Changes the window title to show relevant information, such as whether it's paused or running, the line, the modes, the rule, etc...
        screen.blit(text_running, (text_x - text_running.get_width() // 2, int((height/20)*4.5) - text_running.get_height() // 2))       # render the RUNNING text
    else:                                                                           # If the game is not unpaused, it's paused
        pg.display.set_caption("Cellular Elementary Automata - " + str(celX) + "x" + str(tlines) + " - Rule: " + str(rule) + " - " + rulesetbin + " - PAUSED - " + "{ft}".format(ft="FromTop - " if ftop else "") + "{rv}".format(rv="RuleView - " if rulemode else "") + "{tb}".format(tb="Turbo - " if turbo else "") + "LINE " + str(line))   # Changes the window title to show relevant information, such as whether it's paused or running, the line, the modes, the rule, etc...
        screen.blit(text_paused, (text_x - text_paused.get_width() // 2, int((height/20)*4.5) - text_paused.get_height() // 2))          # render the PAUSE text

def update():     # Function to update the game
    global bg, frame, record        # Set these variables as global
    screen.fill(bg)                 # We fill the screen with the background to clean everything
    update_text()                   # We call the update_text function to update the information displayed by the text
    update_title_run()              # We update the title and the text showing whether it is paused or running
    updategrid()                    # We update the grid and the gameState if not paused
    #if not pause and record: pg.image.save(screen,"out1/" + str(frame) + ".png");frame += 1        # Optional option to record each frame after each update

def events():           # Function that checks the events recorded by PyGame and acts accordingly if some of those events occur
    global gameState, celX,tlines,celw,celh, pause, kill, line, rule, ftop,rulemode, turbo                  # Define these variables as global
    for event in pg.event.get():                                                    # Check for every event recorded by pygame
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not gameState.sum() == 0: pause = not pause  # If the space bar is pressed, the value of game changes, pausing or unpausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: kill = 1          # If the ESC key is pressed, the value if kill changes to TRUE
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: reset()        # If the backspace key is pressed, the game resets:reset()                   # reseting the matrix with zeroes, setting iterations to 0 and pausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_t:ftop = not ftop; reset()# If the t key is pressed, turn FTop changes and reset
        if event.type == pg.KEYDOWN and event.key == pg.K_b and rulemode: turbo = not turbo # If the b key is pressed and we are in RuleMode, turbo changes state
        if event.type == pg.KEYDOWN and event.key == pg.K_r:                        # If the r key is pressed, RuleMode changes state
            rulemode = not rulemode
            if rulemode:ftop = 1; reset();rule = 0;setrule(rule)                    # If it activates, activate ftop, reset, set rule to 0 and updat it
            elif not rulemode: rule = 30;setrule(rule); ftop = 0; reset()           # If it deactivates, deactivate ftop, reset, set rule to default and update it
        if event.type == pg.KEYDOWN and event.key == pg.K_f and (not rulemode or pause): # If the f key is pressed, decrease rule, update it and reset
            rule -=1; setrule(rule); reset()
        if event.type == pg.KEYDOWN and event.key == pg.K_g and (not rulemode or pause): # If the g key is pressed, increase rule, update it and reset
            rule +=1; setrule(rule); reset()
        if event.type == pg.KEYDOWN and event.key == pg.K_w:                        # If W key is pressed:
            tlines += 1; celh = height / tlines                                     # Number of cells in Y increases and we recalcule the height of cells
            celw = celh; celX = round(width/celw)                                   # Set the width and number of rows
            reset()                    # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_s:                        # If S key is pressed:
            tlines -= 1; celh = height / tlines                                     # Number of cells in Y decreases and we recalcule the height of cells
            celw = celh; celX = round(width/celw)                                   # Set the width and number of rows
            reset()                   # Resets the game
        if pg.mouse.get_pressed()[0] == 1 and margin < pg.mouse.get_pos()[0] < width + + margin and margin < pg.mouse.get_pos()[1] < height + margin and ((margin + celh*(tlines-1) < pg.mouse.get_pos()[1]) or (margin + celh*(1) > pg.mouse.get_pos()[1] and ftop) or not line == 0): # If pressing the left button of the mouse, which is stored in a tuple of 3 coordinates, position 0, and it is clicked within the grid, if line is 0, only on the first line:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int((cursor[0] - margin)/celw)+extra,int((cursor[1] - margin)/celh)] = 1  # Change to 1 (alive) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part
        if pg.mouse.get_pressed()[2] == 1 and  margin < pg.mouse.get_pos()[0] < width + margin and margin < pg.mouse.get_pos()[1] < height + margin and ((margin + celh*(tlines-1) < pg.mouse.get_pos()[1]) or (margin + celh*(1) > pg.mouse.get_pos()[1] and ftop) or not line == 0): # If pressing the right button of the mouse, which is stored in a tuple of 3 coordinates, position 2, and it is clicked within the grid, if line is 0, only on the first line:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int((cursor[0] - margin)/celw)+extra,int((cursor[1] - margin)/celh)] = 0  # Change to 0 (dead) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part

while not setup:        # Initial setup
    screen = pg.display.set_mode([width + (margin*2) + int((width + (margin*2))/4),height +  (margin*2)]) # Set up the display with size defined by width and height of the grid, plus the border so when cells are drawn it does not get cut off the edges, plus the margins times 2  and plus a fourth of the total previous width to display text.
    # print(width + (margin * 2) + int((width + (margin * 2)) / 4)); print(height + (margin * 2))         # Print the window resolution
    setrule(rule)                                                                                         # Convert rule to binary
    reset()                                                                                               # Reset gameState
    setup = 1                                                                                             # Finish setup

while not kill:     # Main loop of the game, if Kill is TRUE, it does  not excute
    events()        # Execute events function, which checks if an event is happening and establish a consequence
    update()        # Update the game
