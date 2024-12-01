from cmu_graphics import *

#Camden Ray Johnson
#AndrewID: camdenj, Email: camden@cmu.edu

def constructGameControls(app):
    app.exitButton = Button(app.width-25, 0, 25, 25, "red", "X")
    app.numSalmonSlider = Slider(50, 750, "Number of Salmon", 10)
    app.numPollutionSlider = Slider(50, 800, "Number of Pollutors", 10)
    app.infoModeButton = Button(app.width - 200, 750, 100, 50, "salmon", "Info Mode")

def updateButtons(app, mouseX, mouseY):
    if app.exitButton.isInButton(mouseX, mouseY):
        setActiveScreen("start")
    if app.infoModeButton.isInButton(mouseX, mouseY):
        if app.isInfoMode:
            app.isInfoMode = False
            app.infoModeButton.name = "Creative Mode"
        else:
            app.isInfoMode = True
            app.infoModeButton.name = "Info Mode"

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

    def updateSliderFromMouse(self, mouseX):
        circleX = self.leftX + self.offset
        circleY = self.leftY
        sliderRight = self.leftX + Slider.length
        if (circleX<= self.leftX + Slider.length and circleX >= self.leftX):
            self.offset = mouseX-self.leftX
        elif circleX >= sliderRight:
            self.offset = Slider.length-1
        elif circleX <= self.leftX:
            self.offset = 1
        self.percent = self.offset / Slider.length
        self.value = int(self.maxValue * self.percent)
    
    def isInSlider(self, mouseX, mouseY):
        circleX = self.leftX + self.offset
        circleY = self.leftY
        sliderRight = self.leftX + Slider.length
        if distance(mouseX, mouseY, circleX, circleY) <= Slider.radius+5:
            return True
        return False

    @staticmethod
    def getSliders():
        return Slider.listSliders
    
    def drawSlider(self):
        drawLine(self.leftX, self.leftY, self.leftX+Slider.length, self.leftY, fill = "black", lineWidth = 5)
        drawCircle(self.leftX+self.offset, self.leftY, Slider.radius, fill = "pink")
        drawLabel(f"{self.name}: {self.value}", self.leftX+(Slider.length//2), self.leftY+20, size = 16)


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