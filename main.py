from cmu_graphics import *
from testFile import *
import math
from urllib.request import urlopen
from PIL import Image
import random


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

def onAppStart(app):
    app.width = 1440 #Mac screen width
    app.height = 840 #Mac screen height
    app.controlScreenHeight = 150
    app.displayXY  = (0, 0)
    app.numSalmon = 0
    constructControls(app)
    constructBackground(app)
    
    app.setMaxShapeCount(2000)
    app.colorAtPix = ()
    app.sineWave, app.sineDegrees = 0, 0

############################################################
# Game Screen
############################################################

def constructAnimals(app):
    Pollution(app)
    if len(Salmon.getSalmonList()) < app.numSalmonSlider.value:
        Salmon(app)
    elif len(Salmon.getSalmonList()) > app.numSalmonSlider.value:
        Salmon.getSalmonList().pop()


   
def constructBackground(app):
    app.landscapeImage, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/landscape.png", 1)
    app.landscapeImagePIL = loadPILImageLocal("/Users/camdenjohnson/Desktop/Python workspace/landscape.png")
    app.landscapeImageRGB = app.landscapeImagePIL.convert('RGB')

def constructControls(app):
    app.numSalmonSlider = Slider(50, 750, "Number of Salmon", 10)
    
class Slider:
    listSliders = dict()
    radius = 10
    length = 100
    def __init__(self, leftX, leftY, name, maxValue):
        Slider.listSliders[self] = None
        self.leftX, self.leftY = leftX, leftY
        self.offset = 0
        self.percent = 0
        self.maxValue = maxValue
        self.name = name
        self.value = 0

    @staticmethod
    def getSliders():
        return Slider.listSliders
    
    @staticmethod
    def updateSlidersFromMouse(app, mouseX, mouseY):
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
                slider.value = int(slider.maxValue * slider.percent)
            constructAnimals(app)

    def drawSlider(self):
        drawLine(self.leftX, self.leftY, self.leftX+Slider.length, self.leftY, fill = "black", lineWidth = 5)
        drawCircle(self.leftX+self.offset, self.leftY, Slider.radius, fill = "red")
        drawLabel(f"{self.name}: {self.value}", self.leftX, self.leftY+20, size = 16)

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

class Compartment:
    compartmentsMap = dict()

class Mover:
    def isOnColor(self, app, r1, g1, b1, colorTolerance):
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX, self.leftY))
        checkLeft = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX + self.width, self.leftY))
        checkRight = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        checkBottom = self.leftY + self.height <= app.height-app.controlScreenHeight
        return checkLeft and checkRight and checkBottom
    
    def isLegalLoc(self, app):
        r, g, b = self.legalColor
        return self.isOnColor(app, r, g, b, self.colorTolerance)

class Salmon(Mover):
    salmonScale = 4
    salmonImageRight, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmon.png", salmonScale)
    salmonImageLeft, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmonF.png", salmonScale)
    salmonList = []
    maxSalmon = 10
    swimStepSizeX, swimStepSizeY = 2, 10
    legalColor = (46, 109, 246)
    colorTolerance = 2

    def __init__(self, app):
        self.movingRight = True
        while True:
            self.leftX, self.leftY = random.randint(1, app.width), random.randint(1, app.height-app.controlScreenHeight)
            try: 
                self.isLegalLoc(app)
            except:
                continue
            if self.isLegalLoc(app):
                Salmon.salmonList.append(self)
                return

    def drawSalmon(self):
        if self.movingRight:
            drawImage(Salmon.salmonImageRight, self.leftX, self.leftY)
        else:
            drawImage(Salmon.salmonImageLeft, self.leftX, self.leftY)

    def actionStep(self, app):
        self.leftY += random.randint(-1, 1)
        if self.movingRight:
            self.leftX += Salmon.swimStepSizeX
        else:
            self.leftX -= Salmon.swimStepSizeX

        if not self.isLegalLoc(app) and self.movingRight:
            self.movingRight = False
        elif not self.isLegalLoc(app) and not self.movingRight:
            self.movingRight = True

    @staticmethod
    def getSalmonList():
        return Salmon.salmonList
    
class Pollution(Mover):
    listPollution = []
    legalColor = (0, 0, 0)
    colorTolerance = 2


    pollutionImage, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/pollution.png", 4)

    def __init__(self, app):
        while True:
            self.leftX, self.leftY = random.randint(1, app.width), random.randint(1, app.height-app.controlScreenHeight)
            try: 
                self.isLegalLoc(app)
            except:
                continue
            if self.isLegalLoc(app):
                Pollution.listPollution.append(self)
                break
        self.isStatic = False
        self.durationTumble = 50 + random.randint(0, 10)
        self.tumbleCounter = 0
        self.rotation = 0
        self.rotationStep = int(random.randint(-5, 5))

    def __repr__(self):
        return "I am a pollution"
    def drawPollution(self, app):
        drawImage(self.pollutionImage, self.leftX, self.leftY)

    def tubmbleDownStep(self, app):
        self.rotation += self.rotationStep
        self.leftX += random.randint(-1, 10)
        self.leftY += random.randint(-1, 15)
    
    def actionStep(self, app):
        if not self.isStatic and self.tumbleCounter < self.durationTumble:
            self.tubmbleDownStep(app)
            self.tumbleCounter += 1
        elif self.durationTumble == self.tumbleCounter:
            self.isStatic = True

def game_redrawAll(app):
    drawControls(app)
    drawImage("/Users/camdenjohnson/Desktop/Python workspace/landscape.png", 0, 0)

    for salmon in Salmon.getSalmonList():
        salmon.drawSalmon()

    for pollution in Pollution.listPollution:
        pollution.drawPollution(app)

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

def game_onMouseMove(app, mouseX, mouseY):
    app.displayXY = (mouseX, mouseY) #Just a useful utlility to show location 
    #In case the location is out of index
    try:
        app.colorAtPix = app.landscapeImageRGB.getpixel((mouseX, mouseY))  # Get the RGBA Value of the a pixel of an image
    except:
        pass

def game_onMouseDrag(app, mouseX, mouseY):
    Slider.updateSlidersFromMouse(app, mouseX, mouseY)

def game_onStep(app):
    for salmon in Salmon.getSalmonList():
        salmon.actionStep(app)
    for pollution in Pollution.listPollution:
        pollution.actionStep(app)
        

def distance(x1, y1, x2, y2):

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def isSameColor(r, g, b, r1, g1, b1, colorTolerance):
    if abs(r1-r) <= colorTolerance and \
        abs(g1-g) <= colorTolerance and \
        abs(b1-b) <= colorTolerance:
        return True
    return False

############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    app.enterCreativeButton.drawButton()
def start_onScreenActivate(app):
    app.enterCreativeButton = Button(400, 400, 250, 100, "salmon", "Enter Creative Mode")
    app.enterSurvivalButton = Button(700, 400, 100, 100, "lightBlue", "Enter Survival Mode")

def start_onMousePress(app, mouseX, mouseY):
    if app.enterCreativeButton.isInButton(mouseX, mouseY):
        setActiveScreen('game')

def main():
    cmu_graphics.runAppWithScreens(initialScreen = "start")

main()




