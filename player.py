# handles Player object on screen when maze board is drawn

class Player(object):
    # handles Player object, that is, user interactivity
    
    spacing = 5

    def __init__(self, cellSize):
        # stores cell size, position and radius
        self.cellSize = cellSize
        self.radius = max(cellSize/2 - Player.spacing, 1)
        self.x = self.y = self.radius + Player.spacing
        self.speed = 5

    def moveRight(self):
        # moves player right
        self.x += self.speed

    def moveLeft(self):
        # moves player left
        self.x -= self.speed

    def moveUp(self):
        # moves player up
        self.y -= self.speed

    def moveDown(self):
        # moves player down
        self.y += self.speed

    def draw(self, canvas):
        # draws the player
        x, y, radius = self.x, self.y, self.radius
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="green")