# handles interaction between user_main.py, player.py, prim.py and kruskal.py
# also handles drawing the maze boards

from player import *
from random import *
from prim import *
from kruskal import *
from math import *

class Maze(object):
    puzzles = ["kruskal", "prim"]

    def initMaze(rows, cols, value=None):
        # returns 2D Maze Board 
        # copied from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
        a = []
        for row in range(rows):
            for col in range(cols):
                a += [ [value] * cols]
        return a

    def __init__(self, rows, cols, cellSize, width, height, puzzle=""):
        # initializes a type of puzzle randomly only for debugging purposes
        self.rows = rows
        self.cols = cols
        self.board = Maze.initMaze(rows, cols)
        self.cellSize = cellSize
        self.width = width
        self.height = height
        self.player = Player(cellSize)
        self.walls = None
        if puzzle == "":
            puzzle = choice(Maze.puzzles)
        if puzzle == "kruskal":
            self.walls = Kruskal(rows, cols, cellSize, self.board)
        else:
            self.walls = Prim(rows, cols, cellSize, self.board)

    def draw(self, canvas, exitImg):
        # main function which calls another drawing function
        canvas.create_rectangle(0, 0, self.width, self.height, 
                                fill="mint cream")
        self.drawMaze(canvas, exitImg)

    def drawMaze(self, canvas, exitImg):
        # draws the maze and the player
        walls = self.walls
        for wall in walls:
            (x0, y0, x1, y1) = getValues(wall, self.cellSize)
            canvas.create_line(x0, y0, x1, y1, width=2, fill="black")
        self.player.draw(canvas)
        lx = (self.cols - 1) * self.cellSize + self.cellSize/2
        ly = (self.rows - 1) * self.cellSize + self.cellSize/2
        canvas.create_image(lx, ly, image=exitImg)

    def checkBounds(self, x, y):
        # checks for collisions of player with walls or going off the board
        if (((x - self.player.radius < 0) or 
            (x + self.player.radius > self.width)) or 
            ((y - self.player.radius < 0) or 
            (y + self.player.radius > self.height))):
            # off the board check
            return False
        for wall in self.walls:
            ((frow, fcol), (srow, scol)) = wall
            (x0, y0, x1, y1) = getValues(wall, self.cellSize)
            if frow == srow:
                # horizontal wall check
                diff = abs(y - y0)
                if (diff < self.player.radius and 
                    (x0 <= x-self.player.radius <= x1 or 
                    x0 <= x+self.player.radius <= x1)):
                    return False
            if fcol == scol:
                # vertical wall check
                diff = abs(x - x0)
                if (diff < self.player.radius and 
                    (y0 <= y-self.player.radius <= y1 or 
                    y0 <= y+self.player.radius <= y1)):
                    return False
        return True

    def onKeyPressed(self, direction):
        # controls the movement of Player 
        # sends updated values to check if within bounds, and then makes move
        x, y = self.player.x, self.player.y
        if direction == "Up" and self.checkBounds(x, y-self.player.speed):
            self.player.moveUp()
        elif direction == "Down" and self.checkBounds(x, y+self.player.speed):
            self.player.moveDown()
        elif direction == "Right" and self.checkBounds(x+self.player.speed, y):
            self.player.moveRight()
        elif direction == "Left" and self.checkBounds(x-self.player.speed, y):
            self.player.moveLeft()
        if ((self.player.x+self.player.radius>=(self.cols-1)*self.cellSize+self.cellSize/2)
            and (self.player.y+self.player.radius>=(self.rows-1)*self.cellSize+self.cellSize/2)):
            # checks if game is won
            return True

def getValues(wall, cellSize):
    # finds the pixel coordinates of wall
    ((frow, fcol), (srow, scol)) = wall
    x0 = fcol * cellSize
    y0 = frow * cellSize
    x1 = scol * cellSize
    y1 = srow * cellSize
    return (x0, y0, x1, y1)