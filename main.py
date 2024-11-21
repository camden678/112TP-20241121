from cmu_graphics import *
from testFile import *

def main():
    pass

def onAppStart(app):
    app.width = 1440 #Mac screen width
    app.height = 840 #Mac screen height
    app.controlScreenHeight = 150
    app.displayXY  = (0, 0)
    constructControls()
    app.setMaxShapeCount(5000)
    app.compartmentPixelSize = 15
    app.compartmentMatrix = dict()
    constructCompartmentMatrix(app)
    

def drawControls(app):
    drawRect(0, app.height-app.controlScreenHeight, app.width, app.controlScreenHeight, fill = "blue")
    for slider in Slider.getSliders():
        slider.drawSlider()
    for button in Button.getButtons():
        button.drawButton()

    

def constructControls():
    Button(100, 100, 100, 100, "red", "Red")
    Slider(100, 700, "Number of Fish")
    Slider(250, 700, "Number of Poops")
    Slider(400, 700, "Number of Fish")
    Slider(650, 700, "Number of Poops")

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

class Compartment:
    listCompartments = []

class Animal:
    pass
   # listAnimals = []
  #  def __init__(self,)

def redrawAll(app):
    drawControls(app)
    constructCompartmentMatrix(app)
    

    drawLabel(str(app.displayXY), 40, 10)


def constructCompartmentMatrix(app):
    for x in range(0, app.width, app.compartmentPixelSize):
        for y in range(0, app.height - app.controlScreenHeight, app.compartmentPixelSize):
            app.compartmentMatrix[(x, y)] = None
    
def drawCompartmentMatrix(app):
    for coordinate in app.compartmentMatrix:
        x, y = coordinate
        drawRect(x, y, app.compartmentPixelSize, app.compartmentPixelSize, fill = "red")


def onMouseMove(app, mouseX, mouseY):
    app.displayXY = (mouseX, mouseY) #Just a useful utlility to show location 

def onMouseDrag(app, mouseX, mouseY):
    Slider.updateSliders(mouseX, mouseY)

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

main()
runApp()




