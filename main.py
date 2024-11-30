from cmu_graphics import *
from slider import *
from button import *
from movers import *
import math
from urllib.request import urlopen
from PIL import Image
import random
from imagepkg import *

#Camden Ray Johnson
#AndrewID: camdenj, Email: camden@cmu.edu
#The code for the PIL image loaders was adapted from the 15-112 website.
#All photos that are utilized in this file were not created by myself, besides the landscape.png.
#Citations for Photos:
#Yellow Blob: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.reddit.com%2Fr%2Fcartoons%2Fcomments%2F1dwg0tw%2Fneed_help_finding_this_cartoon_one_of_the%2F&psig=AOvVaw1Le-RwQSKPUak18rII6wEj&ust=1732634833434000&source=images&cd=vfe&opi=89978449&ved=0CBcQjhxqFwoTCJC83e_l94kDFQAAAAAdAAAAABAE
#Salmon: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fillustrations%2Fsockeye-salmon&psig=AOvVaw2-p1E5cvVbwLuPGLygn5Zh&ust=1732634857917000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPiw6fvl94kDFQAAAAAdAAAAABAE

def onAppStart(app):
    app.width = 1440 #Mac screen width
    app.height = 840 #Mac screen height
    app.controlScreenHeight = 150
    app.displayXY  = (0, 0)
    app.numSalmon = 0
    app.waterColor = (46, 109, 246)
    app.roadColor = (0, 0, 0)
    app.airColor = (255, 255, 255)
    app.landColor = (50, 113, 65)
    constructControls(app)
    constructBackground(app)
    
    app.setMaxShapeCount(2000)
    app.colorAtPix = ()
    app.sineWave, app.sineDegrees = 0, 0

############################################################
# Game Screen
############################################################

def constructAnimals(app):
    if len(Salmon.getList()) < app.numSalmonSlider.value:
        Salmon(app)
    elif len(Salmon.getList()) > app.numSalmonSlider.value:
        Salmon.getList().pop()
    if len(Pollution.getList()) < app.numPollutionSlider.value:
        Pollution(app)
    elif len(Pollution.getList()) > app.numPollutionSlider.value:
        Pollution.getList().pop()

def constructBackground(app):
    app.landscapeImage, width, height = loadAndResizeCMUImageLocal("/Users/camdenjohnson/Desktop/Python workspace/landscape.png", 1)
    app.landscapeImagePIL = loadPILImageLocal("/Users/camdenjohnson/Desktop/Python workspace/landscape.png")
    app.landscapeImageRGB = app.landscapeImagePIL.convert('RGB')
    constructCompartments(app)

def constructCompartments(app):
    compartments = {"Air":app.airColor, "Water":app.waterColor, "Land":app.landColor, "Road":app.roadColor}
    for compartment in compartments:
        Compartment(compartment, compartments[compartment])

def constructControls(app):
    app.exitButton = Button(app.width-25, 0, 25, 25, "red", "X")
    app.numSalmonSlider = Slider(50, 750, "Number of Salmon", 10)
    app.numPollutionSlider = Slider(50, 800, "Number of Pollutors", 10)
    
class Compartment:
    listCompartments = []
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.listCompartments.append(self)
    
    def isInCompartment(self, mouseX, mouseY, app):
        colorTolerance = 2
        r,g,b = getMouseColor(mouseX, mouseY)
        r1, g1, b1 = self.color
        return isSameColor(r, g, b, r1, g1, b1, colorTolerance)

    @staticmethod
    def getList():
        return Compartment.listCompartments
    
def game_redrawAll(app):
    drawControls(app)
    drawImage("/Users/camdenjohnson/Desktop/Python workspace/landscape.png", 0, 0)
    

    for salmon in Salmon.getList():
        salmon.drawSalmon()

    for pollution in Pollution.listPollution:
        pollution.drawPollution(app)

    app.exitButton.drawButton()
    drawUtils(app)
    if not InfoBox.activeInfoBox == None:
        
        InfoBox.activeInfoBox.drawInfoBox()

def drawUtils(app):   
    drawRect(0, 0, 100, 40, fill = "white")

    drawLabel(str(app.displayXY), 40, 10)
    drawLabel(str(app.colorAtPix), 40, 30)
    if app.colorAtPix != ():
        r, g, b, = app.colorAtPix
        drawRect(90, 30, 10, 10, fill = rgb(r, g, b))

def drawControls(app):
    drawRect(0, app.height-app.controlScreenHeight, app.width, app.controlScreenHeight, fill = "lightBlue")
    for slider in Slider.getSliders():
        slider.drawSlider()
    for button in Button.getButtons():
        button.drawButton()

def game_onMouseMove(app, mouseX, mouseY):
    generateInfoBox(app, mouseX, mouseY)

    app.displayXY = (mouseX, mouseY) #Just a useful utlility to show location 
    #In case the location is out of index
    try:
        app.colorAtPix = app.landscapeImageRGB.getpixel((mouseX, mouseY))  # Get the RGBA Value of the a pixel of an image
    except:
        pass

def game_onMouseDrag(app, mouseX, mouseY):
    Slider.updateSlidersFromMouse(app, mouseX, mouseY)
    constructAnimals(app)

def game_onStep(app):
    for salmon in Salmon.getList():
        salmon.actionStep(app)
    for pollution in Pollution.listPollution:
        pollution.actionStep(app)

def game_onMousePress(app, mouseX, mouseY):
    if app.exitButton.isInButton(mouseX, mouseY):
        setActiveScreen("start")
        
def distance(x1, y1, x2, y2):

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def isSameColor(r, g, b, r1, g1, b1, colorTolerance):
    if abs(r1-r) <= colorTolerance and \
        abs(g1-g) <= colorTolerance and \
        abs(b1-b) <= colorTolerance:
        return True
    return False

def isOnColor(self, app, r1, g1, b1, colorTolerance):
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX, self.leftY))
        checkLeft = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        r, g, b = app.landscapeImageRGB.getpixel((self.leftX + self.width, self.leftY))
        checkRight = isSameColor(r, g, b, r1, g1, b1, colorTolerance)
        checkBottom = self.leftY + self.height <= app.height-app.controlScreenHeight
        return checkLeft and checkRight and checkBottom
    
def getMouseColor(mouseX, mouseY, app):
    try:
        r, g, b = app.landscapeImageRGB.getpixel((mouseX, mouseY))
    except:
        return None
    return r, g, b

class InfoBox:
    info = {"Salmon":"Blah, blah", "Water":"blah blah"}
    activeInfoBox = None
    def __init__(self, app, mouseX, mouseY, name):
        self.width, self.height = 200, 200
        self.leftX, self.leftY = mouseX, mouseY
        self.drawInfoBox = True
        self.name = name
        InfoBox.activeInfoBox = self
        #If its going off in both directions, flip up diagonally
        if mouseX + self.width >= app.width and mouseY + self.height >= app.height:
            self.leftX, self.leftY = self.leftX - self.width, self.leftY - self.height
        #If its going off in the X direction
        elif mouseX + self.width >= app.width:
            self.leftX = self.leftX - self.width
        #If it is going off in the Y direction
        elif mouseY + self.height >= app.height:
            self.leftY = self.leftY - self.height
        self.targeObject = getTargetObject(app, mouseX, mouseY)
        if self.targetObject == None:
            self.drawInfoBox = False
        self.label = self.info[self.targetObject]
    def drawInfoBox(self):
        if self.drawInfoBox:
            drawRect(self.leftX, self.leftY, self.width, self.height, fill = "red")
            drawLabel(self.name, self.width/2+self.leftX, self.height/2+self.leftY)
        
def getTargetObject(app, mouseX, mouseY):
    print(Mover.getList())
    for mover in Mover.getList():
        print(mover, "testing")
        print(mover.isInMover(mouseX, mouseY))
        if mover.isInMover(mouseX, mouseY):
            return mover
    
def generateInfoBox(app, mouseX, mouseY):
    targetObject = getTargetObject(app, mouseX, mouseY)
    if targetObject != None:
        infoBox = InfoBox(mouseX, mouseY, str(targetObject))


############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawLabel("Save the Salmon!", app.width/2, app.height/3, size = 55, font = "grenze", fill = "salmon", bold = True)
    app.enterCreativeButton.drawButton()
    app.enterSurvivalButton.drawButton()

def start_onScreenActivate(app):
    app.enterCreativeButton = Button(400, 400, 250, 100, "salmon", "Enter Creative Mode")
    app.enterSurvivalButton = Button(700, 400, 100, 100, "lightBlue", "Enter Survival Mode")

def start_onMousePress(app, mouseX, mouseY):
    if app.enterCreativeButton.isInButton(mouseX, mouseY):
        setActiveScreen('game')

def main():
    cmu_graphics.runAppWithScreens(initialScreen = "start")

main()
