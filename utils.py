from urllib.request import urlopen
from cmu_graphics import *
from PIL import Image

#Camden Ray Johnson
#AndrewID: camdenj, Email: camden@cmu.edu


def loadAndResizeCMUImageLocal(path, resizeFactor):
    PILImageFull = Image.open(path)
    fullWidth, fullHeight = PILImageFull.size
    width, height = fullWidth//resizeFactor, fullHeight//resizeFactor
    image = PILImageFull.resize((width, height))
    CMUImageReturn = CMUImage(image)
    return CMUImageReturn, width, height 

def loadPILImageLocal(path):
    PILImageFull = Image.open(path)
    return PILImageFull

#This function was taken from the PIL demo through the 15-112 website:
def loadPilImageURL(url):
    # Loads a PIL image (not a CMU image!) from a url:
    return Image.open(urlopen(url))

def drawMultiLineString(string, cx, cy, fontSize, alignLoc, color):
    lines = string.splitlines()
    numLines = len(lines)
    dy = (0.5 * fontSize)
    startY = cy - (dy*(numLines-1))
    drawY, drawX = startY, cx
    for line in lines:
        drawLabel(line.strip(), drawX, drawY, size = fontSize, align = alignLoc, fill = color)
        drawY += 2 * dy
