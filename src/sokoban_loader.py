# sokoban_loader.py
# Camden Johnson
# AndrewID: camdenj

#The following code was taken from Microsoft Copilot.  I used it to access the graphpics package from the parent directory.
import sys
import os
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
#All further code is my own.

from cmu_graphics import CMUImage
from PIL import Image
import pickle, os

COLORS = {
    'red': (175,  71,  68),
    'green': (113, 187, 82),
    'tan': (238, 219, 131),
    'blue': (66, 81, 181),
    'violet': (149, 69, 183), 
    'cyan': (101, 186, 186),
    'brown': (146, 110, 47)
    
    # finish this for green, blue, violet, cyan, brown, and tan
    # where brown is the brown in the brick, and tan is the tan
    # in the player's face.
}

PIECE_COLORS = [ 'red', 'green', 'blue', 'violet', 'cyan' ]

def readPickleFile(path):
    path = "../pickles/"+path[3:]
    with open(path, 'rb') as f:
        return pickle.load(f)

def writePickleFile(path, contents):
    path = "../pickles/"+path[3:]
    with open(path, 'wb') as f:
        pickle.dump(contents, f)

def loadLevel(path):
    path = "../" + path
    #First return a hardcoded level for testing purposes
    if path == None:
        return loadHardcodedLevel()
    #So as to not overwrite the exiting files
    picklePath = path + ".pickle"
    #This try/except is a workaround to make the reading/writing of pickles easy!
    try:
        return readPickleFile(picklePath)
    except FileNotFoundError:
        rows, cols = getRowsCols(path)
        image = loadPILImageLocal(path, 1)

        width, height = image.width, image.height
        dx, dy = width/cols, height/rows
        #Creates a blank list of rows, cols
        resultList =  [["" for i in range(cols)] for j in range(rows)]
        #Creates the iamge dictionary
        imageDict = dict()

        left, top = 0, 0
        bottom, right = dy, dx
        #Crops the cells and generates the list with the appropriate cell types
        for i in range(rows):
            for j in range(cols):
                cellImage = image.crop((left+3, top+3, right-3, bottom-3))
                cellContents = toCellContents(cellImage)
                resultList[i][j] = cellContents
                #Updates the imageDict with new iamges
                if cellContents not in imageDict:
                    imageDict[cellContents] = CMUImage(cellImage)
                left, right = left+dx, right+dx
            top, bottom = top + dy, bottom + dy
            left, right = 0, dx
        #Generates tuple to send to the sokoban_player
        result = (resultList, imageDict)
        #Stores it!
        writePickleFile(picklePath, result) 
        return result

def toCellContents(inputCell):
    cell=inputCell.convert('RGB')
    trackColorCount = dict()
    #Counts the pixels of each color in a cell
    for pixY in range(cell.height):
        for pixX in range(cell.width):
            r,g,b = cell.getpixel((pixX, pixY))
            pixelColor = getColor(r, g, b)
            if pixelColor in trackColorCount:
                trackColorCount[pixelColor] += 1
            else:
                trackColorCount[pixelColor] = 1
    #Returns this dictionary converted to the cell type
    return getCellType(trackColorCount)

def getCellType(trackColorCount):
    #First checks the piece colors to see if it is a piece
    for color in PIECE_COLORS:
        if color in trackColorCount:
            count = trackColorCount[color]
            #For the blocks, the tolerance is 4000 pixels
            if count >= 4000:
                return color[0].lower()
            #For the targets, the tolerance is 600
            elif count >= 600 and "tan" not in trackColorCount:
                return color[0].upper()
    #If it has any Tan
    if "tan" in trackColorCount:
        #If there's more Tan than Brown, it's a player. 
        if trackColorCount["tan"] > trackColorCount['brown']:
            return "p"
        #Otherwise, its a wall
        else:
            return "w"
    #If nothing else applies, its empty
    return '-'

def getColor(r, g, b):
    colorTolerance = 50
    for color in COLORS:
        r1, g1, b1, = COLORS[color]
        if colorDistance(r, g, b, r1, g1, b1) <=colorTolerance:
            return color
#returns the number of rows and cols from the path
def getRowsCols(path):
    rows = path[path.find("-")+1:path.find("x")]
    cols = path[path.find("x")+1:path.find("p")-1]
    return int(rows), int(cols)
    
def colorDistance(r, g, b, r1, g1, b1):
    return ((r-r1)**2 + (b-b1)**2 + (g-g1)**2)**(0.5)

def loadPILImageLocal(path, resizeFactor):
    PILImageFull = Image.open(path)
    fullWidth, fullHeight = PILImageFull.size
    width, height = int(fullWidth/resizeFactor), int(fullHeight/resizeFactor)
    image = PILImageFull.resize((width, height))
    return image

#########################################################
# Test Function
#########################################################

def loadHardcodedLevel():
    level = [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ]
    images = dict()
    return level, images

def testSokobanLoader():
    print('Testing sokoban_loader...')
    files = ['level1-10x10.png',
             'level2-7x9.png',
             'level3-8x6.png',
             'level4-8x6.png']
    
    correctLevels = [
        # level1-10x10.png
        [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ],

        # level2-7x9.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', '-' ],
          [ 'w', 'R', 'G', 'B', 'V', 'w', 'w', 'w', 'w' ],
          [ 'w', 'p', '-', 'r', 'g', 'b', '-', '-', 'w' ],
          [ 'w', 'w', '-', '-', 'v', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', '-', 'w', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level3-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'p', '-', 'w' ],
          [ 'w', '-', 'r', '-', '-', 'w' ],
          [ 'w', 'w', '-', 'w', 'g', 'w' ],
          [ 'w', '-', 'b', 'v', '-', 'w' ],
          [ 'w', '-', '-', 'c', 'B', 'w' ],
          [ 'w', 'C', 'R', 'V', 'G', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level4-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', 'B', 'G', 'p', 'R', 'w' ],
          [ 'w', '-', '-', 'r', '-', 'w' ],
          [ 'w', 'w', 'g', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'b', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ]

    ]

    for i in range(len(files)):
        file = files[i]
        correctLevel = correctLevels[i]
        level, images = loadLevel(file)
        if level != correctLevel:
            print(f'{file} is incorrect!')
            print('Correct result:')
            prettyPrint(correctLevel)
            print('Your result:')
            prettyPrint(level)
            assert(False)
        print(f'  {file} is correct')
    print('Passed!')

def prettyPrint(L):
    for row in L:
        print(row)
if __name__ == '__main__':
    testSokobanLoader()