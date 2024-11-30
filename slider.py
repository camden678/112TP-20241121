from cmu_graphics import *

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

    def drawSlider(self):
        drawLine(self.leftX, self.leftY, self.leftX+Slider.length, self.leftY, fill = "black", lineWidth = 5)
        drawCircle(self.leftX+self.offset, self.leftY, Slider.radius, fill = "pink")
        drawLabel(f"{self.name}: {self.value}", self.leftX+(Slider.length//2), self.leftY+20, size = 16)