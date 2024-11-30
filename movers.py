import math
from urllib.request import urlopen
from PIL import Image
import random
from imagepkg import *
from cmu_graphics import *


class Mover:
    listMovers = []

    def __init__(self):
        self.leftX, self.leftY = 0, 0
        self.width, self.height = 0, 0
        self.name = ""

    def isOnColor(self, app, r1, g1, b1, colorTolerance):
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX, self.leftY))
        checkLeft = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX + self.width, self.leftY))
        checkRight = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        checkBottom = self.leftY + self.height <= app.height-app.controlScreenHeight
        return checkLeft and checkRight and checkBottom
    
    def __repr__(self):
        return "something"

    def isLegalLoc(self, app):
        r, g, b = self.legalColor
        return self.isOnColor(app, r, g, b, self.colorTolerance)
    
    @staticmethod
    def getList():
        return Mover.listMovers
    
    def isInMover(self, mouseX, mouseY):
        if self.leftX <= mouseX and\
            self.leftX + self.width >= mouseX and\
            self.leftY <= mouseY and\
            self.leftY + self.height >= mouseY:
            print("ding")
            return True
        return False
    
class Pollution(Mover):
    listPollution = []
    ID = 0
    legalColor = (0, 0, 0)
    colorTolerance = 2

    pollutionImage, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/pollution.png", 4)

    def __init__(self, app):
        super(). __init__()
        while True:
            self.leftX, self.leftY = random.randint(1, app.width), random.randint(1, app.height-app.controlScreenHeight)
            try: 
                self.isLegalLoc(app)
            except:
                continue
            if self.isLegalLoc(app):
                Pollution.listPollution.append(self)
                Mover.listMovers.append(self)
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
    @staticmethod
    def getList():
        return Pollution.listPollution
    

class Salmon(Mover):
    ID = 0
    salmonScale = 4
    salmonImageRight, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmon.png", salmonScale)
    salmonImageLeft, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/salmonF.png", salmonScale)
    salmonList = []
    maxSalmon = 10
    swimStepSizeX, swimStepSizeY = 2, 10
    legalColor = (46, 109, 246)
    colorTolerance = 2

    def __init__(self, app):
        super(). __init__()
        self.movingRight = True
        while True:
            self.leftX, self.leftY = random.randint(1, app.width), random.randint(1, app.height-app.controlScreenHeight)
            try: 
                self.isLegalLoc(app)
            except:
                continue
            if self.isLegalLoc(app):
                Salmon.salmonList.append(self)
                Mover.listMovers.append(self)
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
    def getList():
        return Salmon.salmonList
    


def isSameColor(r, g, b, r1, g1, b1, colorTolerance):
    if abs(r1-r) <= colorTolerance and \
        abs(g1-g) <= colorTolerance and \
        abs(b1-b) <= colorTolerance:
        return True
    return False