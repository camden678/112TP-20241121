# sokoban_loader.py

# level files are lightly-edited screenshots from here:
# https://www.sokobanonline.com/play/community/bjertrup/sokomind-plus

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
    with open(path, 'rb') as f:
        return pickle.load(f)

def writePickleFile(path, contents):
    with open(path, 'wb') as f:
        pickle.dump(contents, f)

def loadLevel(path):
    # first return a hardcoded level for testing purposes
    if path == None:
        return loadHardcodedLevel()
    
    picklePath = path + ".pickle"
    try:
        return readPickleFile(picklePath)
    except FileNotFoundError:
        rows, cols = getRowsCols(path)
        image = loadPILImageLocal(path, 1)

        width, height = image.width, image.height
        dx, dy = width/cols, height/rows

        resultList =  [["" for _ in range(cols)] for _ in range(rows)]
        imageDict = dict()

        left, top = 0, 0
        bottom, right = dy, dx
        #print(image.width, image.height, rows, cols, dx, dy)
        for i in range(rows):
            for j in range(cols):
                #print("CELL: ", i, j)
                #print(left, top, right, bottom)
                cellImage = image.crop((left+3, top+3, right-3, bottom-3))
                cellContents = toCellContents(cellImage)
                resultList[i][j] = cellContents
                if cellContents not in imageDict:
                    imageDict[cellContents] = CMUImage(cellImage)
                left, right = left+dx, right+dx
            top, bottom = top + dy, bottom + dy
            left, right = 0, dx
        result = (resultList, imageDict)
        writePickleFile(picklePath, result) 
        return result

def toCellContents(inputCell):
    cell=inputCell.convert('RGB')
    trackColorCount = dict()
    for pixY in range(cell.height):
        for pixX in range(cell.width):
            r,g,b = cell.getpixel((pixX, pixY))
           # print(r, g, b)
            pixelColor = getColor(r, g, b)
          #  print(pixelColor)
            if pixelColor in trackColorCount:
                trackColorCount[pixelColor] += 1
            else:
                trackColorCount[pixelColor] = 1
   # print(trackColorCount)
    return getCellType(trackColorCount)

def getCellType(trackColorCount):
    for color in PIECE_COLORS:
        if color in trackColorCount:
            count = trackColorCount[color]
            if count >= 4000:
                return color[0].lower()
            elif count >= 600 and "tan" not in trackColorCount:
                return color[0].upper()
    
    if "tan" in trackColorCount:
        if trackColorCount["tan"] > trackColorCount['brown']:
            return "p"
        else:
            return "w"

    return '-'

def getColor(r, g, b):
    colorTolerance = 50
    for color in COLORS:
        r1, g1, b1, = COLORS[color]
        if colorDistance(r, g, b, r1, g1, b1) <=colorTolerance:
            return color

def getRowsCols(path):
    rows = path[path.find("-")+1:path.find("x")]
    cols = path[path.find("x")+1:path.find(".")]
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