class Animal:
    #Properties of animals
    pass



class Fish (Animal):

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.alive = True
    def swim(self):
        dx, dy = random