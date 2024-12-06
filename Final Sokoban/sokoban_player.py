# sokoban_player.py
# Camden Johnson
# AndrewID: camdenj

from cmu_graphics import *
from sokoban_loader import *
import copy

def onAppStart(app, useHardCodedLevel):
    app.useHardCodedLevel = useHardCodedLevel
    app.activeLevel = 1
    app.width, app.height = 600, 600
    loadActiveLevel(app)
    app.isWonBool = False
    

def loadActiveLevel(app):
    app.cellSize = 50
    files = ['level1-10x10.png',
             'level2-7x9.png',
             'level3-8x6.png',
             'level4-8x6.png']
    app.activeLevelPath = files[app.activeLevel-1]
    app.board, app.images = loadLevel(app.activeLevelPath)
    app.rows, app.cols = getRowsCols(app.activeLevelPath)
    app.width = app.cols * app.cellSize
    #The 75 accounts for the height of the title area.
    app.height = (app.rows * app.cellSize) + 75
    #Captures all of the target spaces in a dict so that they are never overwritten when a player walks on them.
    app.targetSpaces = dict()
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                app.playerRow, app.playerCol = i, j
            if app.board[i][j].isupper():
                app.targetSpaces.update({(i, j) : app.board[i][j]})
    #Captures previous baords in a list.
    app.previousBoards = [copy.deepcopy(app.board)]
    app.moveNumber = 0


def redrawAll(app):
    #Title and information
    drawLabel('Sokoban Player', app.width/2, 20, size=16, bold=True)
    drawLabel(f'Level = {app.activeLevel}', app.width/2, 35, size=14)
    drawLabel("Press u to Undo", app.width/2, 65, size = 14)
    drawLabel("Press 1-4 to Change Levels", app.width/2, 50, size = 14)
    if not app.useHardCodedLevel:
        drawBoard(app)
    else:
        drawHardBoard(app)
    drawLabel("You Won!", app.width/2, app.height/2, size = 50, visible = app.isWonBool, bold = True)

#Updates player coords in the mode.
def updatePlayerCoords(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                app.playerRow, app.playerCol = i, j

#Returns player coords.
def getPlayerCoords(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                return (i, j)

#Draws hardcoded board.
def drawHardBoard(app):
    leftX, leftY = 0, 75
    for i in range(len(app.board)):
        for j in range(len(app.board[i])):
            element = app.board[i][j]
            getDrawFunc(app, element, leftX, leftY)
            leftX += app.cellSize
        leftX = 0
        leftY += app.cellSize

#Runs the appropriate draw function for the hardcoded board.
def getDrawFunc(app, element, x, y):
    colors = { "r":'red', "g": 'green', "b":'blue', "v":'violet', "c":'cyan' }
    if element == "p":
        drawCircle(x, y, app.cellSize/2, fill = "black", align = "left-top")
    elif element == "w":
        drawRect(x, y, app.cellSize, app.cellSize, fill = "burlyWood")
    elif element.isupper():
        drawStar(x, y, app.cellSize/2, 5, fill = colors[element.lower()], align = "left-top")
    elif element.islower():
        drawRect(x, y, app.cellSize, app.cellSize, fill = colors[element])
        drawStar(x, y, app.cellSize/2, 5, fill = "white", align = "left-top")

    

def drawBoard(app):
    leftX, leftY = 0, 75
    for i in range(len(app.board)):
        for j in range(len(app.board[i])):
            element = app.board[i][j]
            #Does not draw blank cells
            if element == "-":
                leftX += app.cellSize
                continue
            #Sets the image to be drawn from the dictionary generated by loadLevel
            image = app.images[element]
            drawImage(image, leftX, leftY, width = app.cellSize, height = app.cellSize)
            leftX += app.cellSize
        leftX = 0
        leftY += app.cellSize

def isLegalPlayerMove(app, drow, dcol):
    nextRow, nextCol = app.playerRow+drow, app.playerCol +dcol
    nextSpace = app.board[nextRow][nextCol]
    #Always allowed to move into empty space
    if nextSpace == "-":
        return True
    #Never allowed to move into wall
    elif nextSpace == "w":
        return False
    #Always allowed to move into target space
    elif nextSpace.isupper():
        return True
    #If moving into a block, check if that's allowed
    else:
        return isLegalBlockMove(app, nextRow, nextCol, drow, dcol)
    
def isLegalBlockMove(app, blockRow, blockCol, drow, dcol):
    nextRow, nextCol = blockRow+drow, blockCol+dcol
    nextSpace = app.board[nextRow][nextCol]
    #Can't move box into a wall
    if nextSpace == "w" or nextSpace.islower():
        return False
    #Can move a box into empty space
    elif nextSpace == "-":
        return True
    #Can move a box into its target
    elif nextSpace.isupper():
        return True
    

def onKeyPress(app, key):
    #Updates the active level and resets the win condition
    if key.isdigit() and int(key) in [1, 2, 3, 4]:
        app.activeLevel = int(key)
        loadActiveLevel(app)
        app.background = "white"
        app.isWonBool = False
        
    #If not frozen, enables motion
    if not app.isWonBool:
        if key in ['right','left','up','down']:
            if key == "right":
                drow, dcol = 0, 1
            elif key == 'left':
                drow, dcol = 0, -1
            elif key == "up":
                drow, dcol = -1, 0
            elif key == "down":
                drow, dcol = 1, 0
            if isLegalPlayerMove(app, drow, dcol):
                updateBoard(app, drow, dcol)
                #Keep track of previous board for the undo feature
                app.previousBoards.append(copy.deepcopy(app.board))
        #Undoes the last move using the move number
        if key == 'u':
            if not len(app.previousBoards) == 1:
                app.board = copy.deepcopy(app.previousBoards[app.moveNumber-1])
                app.previousBoards = copy.deepcopy(app.previousBoards[:app.moveNumber])
                updatePlayerCoords(app)
                app.moveNumber -= 1
        #Loads a hardcoded penultimate move for level 1
        if key == "a" and app.activeLevel == 1:
            app.board = [
    ['-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w'],
    ['-', '-', '-', '-', 'w', 'w', 'w', 'r', 'r', 'w'],
    ['-', '-', '-', '-', 'w', 'p', 'g', 'G', 'b', 'w'],
    ['-', '-', '-', '-', 'w', '-', '-', 'r', 'r', 'w'],
    ['w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w'],
    ['w', '-', '-', '-', '-', '-', '-', 'w', 'w', 'w'],
    ['w', 'w', '-', '-', '-', '-', '-', '-', '-', 'w'],
    ['-', 'w', '-', '-', '-', 'w', '-', 'w', '-', 'w'],
    ['-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w'],
    ['-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
            ]
            updatePlayerCoords(app)
        

def updateBoard(app, drow, dcol):
    nextRow, nextCol = app.playerRow+drow, app.playerCol +dcol
    nextSpace = app.board[nextRow][nextCol]    
    #If the player is just moving around
    if nextSpace == "-" or nextSpace.isupper():
        app.board[nextRow][nextCol] = 'p'
        app.board[app.playerRow][app.playerCol] = "-"
        #Updates the target spaces if the player was moving over them.
        if (app.playerRow, app.playerCol) in app.targetSpaces:
            app.board[app.playerRow][app.playerCol] = app.targetSpaces[(app.playerRow, app.playerCol)]
        #Update player location
        app.playerRow, app.playerCol = nextRow, nextCol
        
    #If the player is pushing a block
    elif nextSpace.islower():
        app.board[nextRow][nextCol] = 'p'
        #Updates the target spaces if the player was moving over them.
        if (app.playerRow, app.playerCol) in app.targetSpaces:
            app.board[app.playerRow][app.playerCol] = app.targetSpaces[(app.playerRow, app.playerCol)]
        else:
            app.board[app.playerRow][app.playerCol] = "-"
        #Update the player location and block location
        app.playerRow, app.playerCol = nextRow, nextCol
        newBlockRow, newBlockCol = app.playerRow+drow, app.playerCol+dcol
        app.board[newBlockRow][newBlockCol] = nextSpace
    #Incremenents move number
    app.moveNumber += 1
    if isWon(app):
        app.background = "red"

def isWon(app):
    #If the player is on a target, we can't have won
    if (app.playerRow, app.playerCol) in app.targetSpaces:
        return False
    #If there are no more targets, we've won!
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j].isupper():
                app.isWonBool = False
                return False
    app.isWonBool = True
    return True


runApp(600, 600, useHardCodedLevel = False)
