# color_viewer.py

from cmu_graphics import *
from PIL import Image

def onAppStart(app, path):
    app.path = path
    app.width, app.height = 750, 750
    app.levelPILImage= loadPILImageLocal(app.path, 1.2)
    app.levelRGBImage = app.levelPILImage.convert('RGB')
    app.levelCMUImage = CMUImage(app.levelPILImage)
    app.mouseCoords = (0, 0)
    app.mouseColor = (0, 0, 0)

def redrawAll(app):
    drawLabel('Color Viewer', app.width/2, 20, size=16, bold=True)
    drawLabel(f'file = {app.path}', app.width/2, 35, size=14)
    drawLabel(str(app.mouseCoords) + str(app.mouseColor), app.width/2, 50, size = 14)
    drawImage(app.levelCMUImage, app.width/2, (app.height/2)+25, align='center')

def getPixel(app, x, y):
    image = app.levelRGBImage
    leftX, rightX = app.width/2 -  image.width/2, app.width/2 + image.width/2
    bottomY, topY = app.height/2 +  image.height/2, app.height/2 - image.height/2
    if x >= leftX and x<= rightX and y>=topY and y<=bottomY:
        imageX = x-leftX
        imageY = y-topY
        r,g,b = app.levelRGBImage.getpixel((imageX,imageY))
        return r, g, b


def onMouseMove(app, mouseX, mouseY):
    app.mouseCoords = (mouseX, mouseY)
    pix = getPixel(app, mouseX, mouseY)
    if pix != None:
        app.mouseColor = pix

def loadPILImageLocal(path, resizeFactor):
    PILImageFull = Image.open(path)
    fullWidth, fullHeight = PILImageFull.size
    width, height = int(fullWidth/resizeFactor), int(fullHeight/resizeFactor)
    image = PILImageFull.resize((width, height))
    return image

runApp(path='level3-8x6.png')