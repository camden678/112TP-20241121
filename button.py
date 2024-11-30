from cmu_graphics import *

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