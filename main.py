from cmu_graphics import *
from testFile import *

def main():
    pass

def onAppStart(app):
    app.width = 1440 #Mac screen width
    app.height = 840 #Mac screen height
    app.displayXY  = (0, 0)
    constructControls()

def drawControls(app):
    drawRect(0, app.height-200, app.width, 200, fill = "blue")
    for slider in Slider.getSliders():
        slider.drawSlider()

def constructControls():
    Slider(400, 400, "Number of Fish")
    Slider(50, 400, "Number of Poops")

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

def redrawAll(app):
    drawLabel(str(app.displayXY), 40, 10)
    drawControls(app)

def onMouseMove(app, mouseX, mouseY):
    app.displayXY = (mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    Slider.updateSliders(mouseX, mouseY)

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

main()
runApp()




