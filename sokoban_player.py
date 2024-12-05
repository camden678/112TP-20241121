# sokoban_player.py

from cmu_graphics import *
from sokoban_loader import *
import copy

def onAppStart(app):
    app.activeLevel = 1
   
    app.width, app.height = 600, 600
    loadActiveLevel(app)
    
    
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
    app.height = (app.rows * app.cellSize) + 75
    app.playerSavedSpace = "-"
    app.blockSavedSpace = "-"
    app.targetSpaces = dict()
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                app.playerRow, app.playerCol = i, j
            if app.board[i][j].isupper():
                app.targetSpaces.update({(i, j) : app.board[i][j]})
    app.previousBoards = [copy.deepcopy(app.board)]
    app.moveNumber = 0
    prettyPrint(app.board)


def redrawAll(app):
    if not app.isHardCoded:
        drawBoard(app)
    else:
        drawHardBoard(app)

def updatePlayerCoords(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                app.playerRow, app.playerCol = i, j

def getPlayerCoords(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == "p":
                return (i, j)

def drawHardBoard(app):
    leftX, leftY = 0, 75
    
    for i in range(len(app.board)):
        for j in range(len(app.board[i])):
            element = app.board[i][j]
            getDrawFunc(app, element)
            leftX += app.cellSize
        leftX = 0
        leftY += app.cellSize

def getDrawFunc(app, element, x, y):
    if element == "p":
        return drawCircle(x, y, 50, fill = "black")
    elif element == "w":
        return drawRect(x, y, 90, 90, fill = "burlyWood")
    if element.isupper():
        colors = { "r":'red', "g": 'green', "b":'blue', "v":'violet', "c":'cyan' }
        return drawStar(x, y, 50, 5, fill = colors[element])
    elif element.islower():

    

def drawBoard(app):
    leftX, leftY = 0, 75
    
    for i in range(len(app.board)):
        for j in range(len(app.board[i])):
            element = app.board[i][j]
            image = app.images[element]
            drawImage(image, leftX, leftY, width = app.cellSize, height = app.cellSize)
            leftX += app.cellSize
        leftX = 0
        leftY += app.cellSize

def isLegalPlayerMove(app, drow, dcol):
    nextRow, nextCol = app.playerRow+drow, app.playerCol +dcol
    nextSpace = app.board[nextRow][nextCol]
    if nextSpace == "-":
        return True
    elif nextSpace == "w":
        return False
    elif nextSpace.isupper():
        return True
    else:
        return isLegalBlockMove(app, nextRow, nextCol, drow, dcol)
    
def isLegalBlockMove(app, blockRow, blockCol, drow, dcol):
    nextRow, nextCol = blockRow+drow, blockCol+dcol
    nextSpace = app.board[nextRow][nextCol]
    if nextSpace == "w" or nextSpace.islower():
        return False
    elif nextSpace == "-":
        return True
    elif nextSpace.isupper():
        return True
    

def onKeyPress(app, key):
    if key.isdigit() and int(key) in [1, 2, 3, 4]:
        app.activeLevel = int(key)
        loadActiveLevel(app)
        app.background = "white"
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
            app.previousBoards.append(copy.deepcopy(app.board))
    if key == 'u':
        if not len(app.previousBoards) == 1:
            app.board = copy.deepcopy(app.previousBoards[app.moveNumber-1])
            app.previousBoards = copy.deepcopy(app.previousBoards[:app.moveNumber])
            updatePlayerCoords(app)
            app.moveNumber -= 1
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
    #just moving around
    if nextSpace == "-" or nextSpace.isupper():
        app.board[nextRow][nextCol] = 'p'
        app.board[app.playerRow][app.playerCol] = "-"
        if (app.playerRow, app.playerCol) in app.targetSpaces:
            app.board[app.playerRow][app.playerCol] = app.targetSpaces[(app.playerRow, app.playerCol)]
        app.playerRow, app.playerCol = nextRow, nextCol
        
    #pushing a block
    elif nextSpace.islower():
        app.board[nextRow][nextCol] = 'p'
        if (app.playerRow, app.playerCol) in app.targetSpaces:
            app.board[app.playerRow][app.playerCol] = app.targetSpaces[(app.playerRow, app.playerCol)]
        else:
            app.board[app.playerRow][app.playerCol] = "-"
        app.playerRow, app.playerCol = nextRow, nextCol

        newBlockRow, newBlockCol = app.playerRow+drow, app.playerCol+dcol
        app.board[newBlockRow][newBlockCol] = nextSpace
    app.moveNumber += 1

    if isWon(app):
        app.background = "red"

def isWon(app):
    if (app.playerRow, app.playerCol) in app.targetSpaces:
        return False

    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j].isupper():
                return False
    return True


runApp()

