from cmu_graphics import *
from testFile import *
import math
from urllib.request import urlopen
from PIL import Image

def loadPilImageLocal(path):
    return Image.open(path)

#This function was taken from the PIL demo through the 15-112 website:
def loadPilImageURL(url):

    # Loads a PIL image (not a CMU image!) from a url:
    return Image.open(urlopen(url))

def onAppStart(app):
    app.width = 1440 #Mac screen width
    app.height = 840 #Mac screen height
    app.controlScreenHeight = 150
    app.displayXY  = (0, 0)
    constructControls(app)
    constructAnimals(app)
    constructBackground(app)
    app.setMaxShapeCount(5000)
    app.colorAtPix = ()
    app.sineWave, app.sineDegrees = 0, 0
   
def constructBackground(app):
    app.landscapeImage = loadPilImageLocal("/Users/camdenjohnson/Desktop/Python workspace/landscape.png")
    app.landscapeImageRGB = app.landscapeImage.convert('RGB')

def constructControls(app):
    Button(1000, 600, 100, 100, "red", "Red")
    Slider(100, 700, "Number of Fish")
    Slider(250, 700, "Number of Poops")
    Slider(400, 700, "Number of Fish")
    Slider(650, 700, "Number of Poops")

def constructAnimals(app):
    Salmon(700, 520)
    Salmon(500, 500)
    
class Slider:
    listSliders = []
    radius = 10
    length = 100
    def __init__(self, leftX, leftY, name):
        Slider.listSliders.append(self)
        self.leftX, self.leftY = leftX, leftY
        self.offset = 0
        self.percent = 0
        self.name = name
   
    @staticmethod
    def getSliders():
        return Slider.listSliders
    
    @staticmethod
    def updateSliders(mouseX, mouseY):
        for slider in Slider.getSliders():
            circleX = slider.leftX + slider.offset
            circleY = slider.leftY
            sliderRight = slider.leftX + Slider.length
            if distance(mouseX, mouseY, circleX, circleY) <= Slider.radius+5:
                if (circleX<= slider.leftX + Slider.length and circleX >= slider.leftX):
                    slider.offset = mouseX-slider.leftX
                elif circleX >= sliderRight:
                    slider.offset = Slider.length-1
                elif circleX <= slider.leftX:
                    slider.offset = 1
            slider.percent = slider.offset / Slider.length
   
    def drawSlider(self):
        drawLine(self.leftX, self.leftY, self.leftX+Slider.length, self.leftY, fill = "black", lineWidth = 5)
        drawCircle(self.leftX+self.offset, self.leftY, Slider.radius, fill = "red")
        drawLabel(self.name + str(self.percent), self.leftX, self.leftY+20, size = 16)

class Button:
    listButtons = []
    def __init__(self, leftX, leftY, width, height, color, name):
        Button.listButtons.append(self)
        self.leftX, self.leftY = leftX, leftY
        self.width, self.height = width, height
        self.color = color
        self.name = name
    
    def drawButton(self):
        drawRect(self.leftX, self.leftY, self.width, self.height, fill = self.color)
        drawLabel(self.name, self.width/2 + self.leftX, self.height/2 + self.leftY, size = 16)

    @staticmethod
    def getButtons():
        return Button.listButtons
    
    def isInButton(self, mouseX, mouseY):
        if self.leftX <= mouseX <= self.leftX + self.width and \
            self.leftY <= mouseY <= self.leftY + self.height:
            return True
        return False

class Animal:
    pass

class Salmon(Animal):

    salmonScale = 4
    salmonImageRightFull = loadPilImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmon.png")
    salmonWidth, salmonHeight = salmonImageRightFull.size
    salmonImageRight = salmonImageRightFull.resize((salmonWidth//salmonScale, salmonHeight//salmonScale))
    salmonImageLeftFull = loadPilImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmonF.png")
    salmonImageLeft = salmonImageLeftFull.resize((salmonWidth//salmonScale, salmonHeight//salmonScale))
    salmonList = []
    swimStepSizeX, swimStepSizeY = 2, 2

    def __init__(self, x, y):
        Salmon.salmonList.append(self)
        self.leftX, self.leftY = x, y
        self.movingRight = True
        
    def isInWater(self, app):
        colorTolerance = 5
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX, self.leftY))
        r1, g1, b1 = 46, 109, 246 #This is the blue color that is being used in the testLandscape
        checkLeft = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX + Salmon.salmonWidth, self.leftY))
        checkRight = isSameColor(r, g, b, r1, g1, b1, colorTolerance)

        if checkLeft and checkRight:
            return True
        return False

    def drawSalmon(self):
        if self.movingRight:
            drawImage(CMUImage(Salmon.salmonImageRight), self.leftX, self.leftY)
        else:
            drawImage(CMUImage(Salmon.salmonImageLeft), self.leftX, self.leftY)

    def swimStep(self, app):
        self.leftY += app.sineWave * Salmon.swimStepSizeX
        if self.movingRight:
            self.leftX += Salmon.swimStepSizeX
        else:
            self.leftX -= Salmon.swimStepSizeX

        if not self.isInWater(app) and self.movingRight:
            self.movingRight = False
        elif not self.isInWater(app) and not self.movingRight:
            self.movingRight = True

    @staticmethod
    def getSalmonList():
        return Salmon.salmonList

def redrawAll(app):
    drawControls(app)
    drawImage("/Users/camdenjohnson/Desktop/Python workspace/landscape.png", 0, 0)
    for salmon in Salmon.getSalmonList():
        salmon.drawSalmon()

    drawUtils(app)

def drawUtils(app):   
    drawRect(0, 0, 100, 40, fill = "white")

    drawLabel(str(app.displayXY), 40, 10)
    drawLabel(str(app.colorAtPix), 40, 30)
    if app.colorAtPix != ():
        r, g, b, = app.colorAtPix
        drawRect(90, 30, 10, 10, fill = rgb(r, g, b))

def drawControls(app):
    drawRect(0, app.height-app.controlScreenHeight, app.width, app.controlScreenHeight, fill = "blue")
    for slider in Slider.getSliders():
        slider.drawSlider()
    for button in Button.getButtons():
        button.drawButton()

def onMouseMove(app, mouseX, mouseY):
    app.displayXY = (mouseX, mouseY) #Just a useful utlility to show location 
    #im = Image.open('pond.jpg') # Can be many different formats.
    #pix = im.load()
    try:
        app.colorAtPix = app.landscapeImageRGB.getpixel((mouseX, mouseY))  # Get the RGBA Value of the a pixel of an image
    except:
        pass

def onMouseDrag(app, mouseX, mouseY):
    Slider.updateSliders(mouseX, mouseY)

def onStep(app):
    app.sineDegrees +=1
    if app.sineDegrees == 360:
        app.sineDegrees = 0
    app.sineWave = math.sin(app.sineDegrees*10)
    for salmon in Salmon.getSalmonList():
        salmon.swimStep(app)

def distance(x1, y1, x2, y2):

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def isSameColor(r, g, b, r1, g1, b1, colorTolerance):
    if abs(r1-r) <= colorTolerance and \
        abs(g1-g) <= colorTolerance and \
        abs(b1-b) <= colorTolerance:
        return True
    return False

runApp()




