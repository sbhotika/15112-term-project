# main function to generate mazes using Prim's algorithm
# Based on Randomnized Prim's algorithm at
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim.27s_algorithm

from random import *
from math import *

def Prim(rows, cols, cellSize, board):
    # main function to generate maze according to Prim's algorithm
    allWalls = makeWalls(rows, cols)

    def getWalls():
        # only returns the final walls after maze generation is finished
        return finalWalls

    def generateMaze(board, allWalls, rows, cols):
        # handles main execution of Prim's, by iterating through all walls
        # picking random wall; if exactly one unvisited cell on either side,
        # add cell to path, and remove wall
        startCell = (0, 0)
        walls = [ ]
        walls.extend(addWalls(allWalls, startCell))
        visited = set()
        path = set()
        visited.add(startCell)

        while len(walls) != 0:
            # runs until all walls not gone through
            # pick random wall
            wall = choice(walls)
            ((frow, fcol), (srow, scol)) = wall
            walls.remove(wall)

            if ((frow == 0 and srow == 0) or (fcol == 0 and scol == 0)):
                # border walls
                # go to next iteration
                continue
            else:
                fCell = sCell = None
                # assigning values to firstCell and secondCell so 
                # python doesn't get upset with me
                
                if fcol == scol:
                    # vertical wall
                    srow, scol = frow, fcol-1
                    fCell = (frow, fcol)
                    sCell = (srow, scol)
                elif frow == srow:
                    # horizontal wall
                    srow, scol = frow-1, fcol
                    fCell = (frow, fcol)
                    sCell = (srow, scol)
                
                if ((fCell in visited and sCell not in visited) 
                    or (fCell not in visited and sCell in visited)):
                    # if exactly one bordering cell is unvisited
                    # add cells to maze, make wall a path, and add new walls
                    path.add(fCell)
                    path.add(sCell)
                    visited.add(fCell)
                    visited.add(sCell)
                    allWalls.remove(wall)
                    walls.extend(addWalls(allWalls, fCell))
                    walls.extend(addWalls(allWalls, sCell))
        return allWalls

    finalWalls = generateMaze(board, allWalls, rows, cols)
    return getWalls()

def makeWalls(rows, cols):
    # make walls for entire board
    # repeated code from kruskal.py
    walls = set()
    for row in range(rows):
        for col in range(cols):
            top =  ((row, col), (  row, col+1 ))
            left = ((row, col), (row+1, col   ))
            walls.add(top)
            walls.add(left)
    return walls

def addWalls(allWalls, cell):
    # add walls of cell if valid and present in allWalls that have not been 
    # looked at yet
    (row, col) = cell
    walls = []
    top =    ((  row, col  ), (  row, col+1))
    right =  ((  row, col  ), (row+1, col  ))
    left =   ((  row, col+1), (row+1, col+1))
    bottom = ((row+1, col  ), (row+1, col+1))
    if top in allWalls:
        walls += [top]
    if right in allWalls:
        walls += [right]
    if left in allWalls:
        walls += [left]
    if bottom in allWalls:
        walls += [bottom]
    return walls

def isValidCell(board, cell):
    # checks if cell on board
    (row, col) = cell
    rows, cols = len(board), len(board[0])
    if 0 <= row < rows and 0 <= col < cols:
        return True
    return False
