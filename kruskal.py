# main function to generate mazes using Kruskal's algorithm
# based on Randomnized Kruskal's algorithm found at
# https://en.wikipedia.org/wiki/Maze_generation_algorithm

from random import *


def Kruskal(rows, cols, cellSize, board):
    # main function
    (maze, walls) = generateMaze(board, rows, cols)
    return walls

def generateMaze(board, rows, cols):
    # generates maze by making board full of walls and then iterating through
    # randomly
    walls = makeWalls(board, rows, cols)
    (maze, walls) = randomMaze(board, walls, rows, cols)
    return (maze, walls)

def makeWalls(board, rows, cols):
    # make walls for entire board
    walls = [ ]
    for row in range(rows):
        for col in range(cols):
            top = ((row, col), (row, col+1))
            left = ((row, col), (row+1, col))
            walls += [top, left]
            board[row][col] = KruskalSet(row, col)
    return walls

def randomMaze(board, walls, rows, cols):
    # iterate through walls randomly and make path if cells on both sides
    # belong to distinct sets, then remove wall
    shuffle(walls)
    wallSet = set(walls)
    for wall in walls:
        ((frow, fcol), (srow, scol)) = wall
        if ((frow == 0 and srow == 0) or (fcol == 0 and scol == 0)):
            # border wall
            wallSet.remove(wall)
            continue
        else:
            fCell = sCell = None
            # assigning values to firstCell and secondCell so python doesn't get
            # upset with me
            if fcol == scol:
                # vertical wall
                srow, scol = frow, fcol-1
                fCell = board[frow][fcol]
                sCell = board[srow][scol]
            elif frow == srow:
                # horizontal wall
                srow, scol = frow-1, fcol
                fCell = board[frow][fcol]
                sCell = board[srow][scol]

            if fCell.distinctFrom(sCell):
                # if both sets fully distinct then join fully
                # joining both ways to be safe then removing wall from allWalls
                # so it won't be added again
                board[frow][fcol].joinSets(board[srow][scol], board)
                board[srow][scol].joinSets(board[frow][fcol], board)
                wallSet.remove(wall)
        
    walls = list(wallSet)
    return (board, walls)

class KruskalSet(object):
    # handles creating a set for each cell on board, checking if distinct from
    # another set, and completely joining two different sets
    def __init__(self, row, col):
        self.cell = (row, col)
        self.set = set({self.cell})
        self.joined = False

    def distinctFrom(self, other):
        # checks if one set completely distinct from another set
        if (len(self.set & other.set) == 0):
            return True
        return False

    def joinSets(self, other, board):
        # joins the sets of two cells which were previously distinct
        updateCells = []
        for elem in other.set:
            # iterates through all cells and adds them to another list
            self.set.update({elem})
            updateCells.append(elem)
        for elem in updateCells:
            # for every element, updates the set of each value, using objects
            (row, col) = elem
            board[row][col].set.update(self.set)
        other.set = self.set
        self.joined = other.joined = True

def isValid(board, rows, cols, maybeCell):
    # adapted from https://www.cs.cmu.edu/~112/notes/maze-solver.py
    # checks if cell is on board
    (row, col) = maybeCell
    if 0 <= row < rows and 0 <= col < cols:
        return True
    return False