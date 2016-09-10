# events-example0.py
# copied from https://www.cs.cmu.edu/~112/notes/events-example0.py
# Super Maze! from Shubhangi Bhotika + sbhotika
# all algorithms were based on those found at:
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# the images were found on the Google
# the buttons were drawn using this very handy website:
# http://dabuttonfactory.com/

from tkinter import *
from random import *
from Maze import *

class Puzzle(object):
    # handles interaction with Maze
    def __init__(self, rows, cols, cellSize, width, height, puzzle=""):
        self.rows = rows
        self.cols = cols
        self.cellSize = cellSize
        self.game = Maze(rows, cols, cellSize, width, height, puzzle)


##########################################################################

def instructions(data):
    # stores instructions for maze
    data.mazeInstructions = """
    Find your way from
    beginning to finish. 
    Use arrows to move the ball and 
    help navigate its way to the finish line
    (where the flag is). 
    Press 'i' for instructions, 
    'r' to restart, and 'q' 
    to quit the game 
    (apart from the buttons). 
    The goal is to find the finish
    as fast as possible. 
    Press anywhere on screen 
    to go back to main menu.
    """

def init(data):
    # load data.xyz as appropriate
    data.gameOver = data.gamePaused = data.instructions = data.gameWon = False
    data.kruskalPlay = data.primPlay = False
    data.menu = True
    data.score = data.time = 0
    data.margin = 100
    data.cellSize = min((data.width-data.margin)/data.cols, 
                        (data.height-data.margin)/data.rows)
    data.kruskalPuzzle = Puzzle(data.rows, data.cols, data.cellSize, 
                        data.width-data.margin, data.height-data.margin,
                        "kruskal")
    data.primPuzzle = Puzzle(data.rows, data.cols, data.cellSize, 
                        data.width-data.margin, data.height-data.margin,
                        "prim")
    instructions(data)
    loadImages(data)

def loadImages(data):
    # load images into data so I can make my game look pretty later
    data.helpBtn = PhotoImage(file="images/help.png")
    data.pauseBtn = PhotoImage(file="images/pause.png")
    data.restartBtn = PhotoImage(file="images/restart.png")
    data.kruskalBtn = PhotoImage(file="images/kruskal.png")
    data.primBtn = PhotoImage(file="images/prim.png")
    data.instructionsBtn = PhotoImage(file="images/instructions.png")
    data.maze_bg = PhotoImage(file="images/maze_bg.png")
    data.exit = PhotoImage(file="images/exit.png")
    data.backBtn = PhotoImage(file="images/back.png")


def mousePressed(event, data):
    # use event.x and event.y
    if (data.menu == False or data.primPlay or data.kruskalPlay 
        and data.instructions and 
        (0 <= event.x <= data.width) and 
        (0 <= event.y <= data.height)):
        # removes instructions screen
        data.instructions = False
        if data.kruskalPlay == False and data.primPlay == False: data.menu = True
    if (data.menu and data.instructions == False 
        and 175 <= event.x <= 525 and 120 <= event.y <= 205):
        # toggles instructions screen
        data.instructions = True
        data.menu = False

    if (data.menu and data.instructions == False 
        and 175 <= event.x <= 525 and 285 <= event.y <= 355):
        # checks if Kruskal button selected on main screen
        data.kruskalPlay = True
        data.menu = False

    if (data.menu and data.instructions == False
        and 175 <= event.x <= 525 and 420 <= event.y <= 505):
        # checks if Prim button selected on main screen
        data.primPlay = True
        data.menu = False

    if (data.gameWon and 235 <= event.x <= 470 
        and 540 <= event.y <= 610):
        # checks if back to main menu option selected on game won screen
        # and then re-initializes new puzzle for user
        data.gameWon = False
        data.menu = True
        if data.kruskalPlay: 
            data.kruskalPlay = False
            data.kruskalPuzzle = Puzzle(data.rows, data.cols, data.cellSize, 
                            data.width-data.margin, data.height-data.margin,
                            "kruskal")
        if data.primPlay: 
            data.primPlay = False
            data.primPuzzle = Puzzle(data.rows, data.cols, data.cellSize, 
                            data.width-data.margin, data.height-data.margin,
                            "prim")

    if (data.gameWon == False and
        data.instructions == False and 
        (data.primPlay or data.kruskalPlay) and data.gameOver == False):
        if (data.gamePaused == False and 
            625 <= event.x <= 675 and 125 <= event.y <= 152):
            data.instructions = True

        if (data.gamePaused and 0 <= event.x <= data.width and 
            0 <= event.y <= data.height):
            data.gamePaused = False

        if (625 <= event.x <= 675 and 180 <= event.y <= 210):
            data.gamePaused = True

        if (data.gamePaused == False and 630 <= event.x <= 655
            and 250 <= event.y <= 300):
            init(data)
            return None
        


def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.char == "r"):
        # restarts game
        init(data)
        return None
    if (event.char == "q"):
        # quits game
        data.gameOver = True
    if (event.char == "p") and (data.gameOver == False):
        # pauses or un-pauses game if game is not over
        data.gamePaused = not(data.gamePaused)
    if (data.gameOver == False and data.menu == False and 
        data.gamePaused == False and data.instructions == False):
            if (event.keysym == "Up" or event.keysym == "Down" or 
                event.keysym == "Right" or event.keysym == "Left"):
                move = None
                if data.kruskalPlay:
                    move = data.kruskalPuzzle.game.onKeyPressed(event.keysym)
                elif data.primPuzzle:
                    move = data.primPuzzle.game.onKeyPressed(event.keysym)
                if move == True:
                    data.gameWon = True

def timerFired(data):
    # handles the time elapsed for game
    if (data.kruskalPlay or data.primPlay) and data.gameOver == False:
        data.time += 1

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0,0,data.width,data.height,fill="beige")
    drawBoard(canvas, data)

def drawBoard(canvas, data):
    # checks state of board before drawing
    if data.gameOver:
        drawGameOver(canvas, data)
    elif data.gamePaused:
        drawGamePaused(canvas, data)
    elif data.instructions:
        drawInstructions(canvas, data)
    else:
        canvas.create_image(0, 0, anchor=NW, image=data.maze_bg)
        if data.menu:
            drawMainScreen(canvas, data)
        else:
            drawGame(canvas, data)

def drawMainScreen(canvas, data):
    # got stipple from http://www.kosbie.net/cmu/fall-11/15-112/handouts/
    # misc-demos/src/semi-transparent-stipple-demo.py
    startX, startY = data.width/2, data.height - 80
    # dark slate blue
    canvas.create_text(startX, startY, text="Super Maze!", 
                       font="Georgia 60 bold", fill="gray30")

    startY -= 150
    canvas.create_image(startX, startY, image=data.primBtn)

    startY -= 150
    canvas.create_image(startX, startY, image=data.kruskalBtn)

    startY -= 150
    canvas.create_image(startX, startY, image=data.instructionsBtn)


def drawGameOver(canvas, data):
    # got stipple from http://www.kosbie.net/cmu/fall-11/15-112/handouts/
    # misc-demos/src/semi-transparent-stipple-demo.py
    message = "Press 'r' to \nto restart game"
    score = str(data.score)
    minutes = data.time//60
    seconds = data.time%60
    canvas.create_rectangle(0, 0, data.width, data.height, fill="pink", 
                            stipple="gray75")
    canvas.create_text(data.width/2, 100, text="Game over!", 
                        fill="gray9", font="Georgia 45 bold")
    canvas.create_text(data.width/2, data.height/2, 
                    text="Time: %d:%d \nScore: " % (minutes, seconds) + score, 
                    fill="gray9", font="Georgia 30 bold")
    canvas.create_text(data.width/2, data.height - 80,text=message, 
                        fill="gray9", font="Georgia 30 bold")

def drawGamePaused(canvas, data):
    # got stipple from http://www.kosbie.net/cmu/fall-11/15-112/handouts/
    # misc-demos/src/semi-transparent-stipple-demo.py
    message = """Press 'p' to un-pause game
    or press anywhere on screen"""
    canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan", 
                            stipple="gray75")
    canvas.create_text(data.width/2, data.height/2, text=message, fill="gray9", 
                        font="Georgia 30 bold")

def drawInstructions(canvas, data):
    # draws instructions for puzzles
    message = data.mazeInstructions
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange", 
                            stipple="gray75")
    canvas.create_text(data.width/2, data.height/2, text=message, 
                        fill="gray9", font="Georgia 20 bold")

def drawGame(canvas, data):
    # checks if game has been won or still being played- draws accordingly
    if data.gameWon:
        message = "CONGRATULATIONS!"
        canvas.create_rectangle(0, 0, data.width, data.height, fill="orange", 
                                stipple="gray75")
        canvas.create_text(data.width/2, 100, text=message, 
                            fill="gray9", font="Georgia 30 bold")
        message = "You finished the maze!"
        canvas.create_text(data.width/2, data.height/2, text=message,
                            fill="gray9", font="Georgia 25 bold")
        canvas.create_image(data.width/2, data.height - 100, image=data.backBtn)
    else:
        drawMargins(canvas, data)
        drawPuzzle(canvas, data)

def drawMargins(canvas, data):
    # just branch off to the different margins
    drawRightMargin(canvas, data)
    drawBottomMargin(canvas, data)

def drawPuzzle(canvas, data):
    # draw kruskal or prim
    if data.kruskalPlay:
        data.kruskalPuzzle.game.draw(canvas, data.exit)
    elif data.primPlay:
        data.primPuzzle.game.draw(canvas, data.exit)

def drawRightMargin(canvas, data):
    # draws right margin for playing screen 
    startX = data.width - data.margin
    center = (startX + data.width)/2
    minutes = data.time//60
    seconds = data.time%60
    startY = 40
    fontSize = 25
    canvas.create_text(center, startY, text="Timer:", font="Georgia 10 bold")

    startY += fontSize
    canvas.create_text(center, startY, 
            text= str(minutes) + " mins " + str(seconds) + " secs", 
            font="Georgia 10 bold")

    startY += fontSize
    canvas.create_text(center, startY, text="Score: " + str(data.score), 
                    font="Georgia 10 bold")
    
    createButtons(canvas, data, startX, startY, center)

def createButtons(canvas, data, startX, startY, center):
    # creates buttons on right margin
    buttonSize = 20
    spacing = 40
    startY += buttonSize + spacing
    canvas.create_image(center, startY, image=data.helpBtn)
    
    startY += buttonSize + spacing
    canvas.create_image(center, startY, image=data.pauseBtn)

    startY += buttonSize + spacing
    canvas.create_image(center, startY, image=data.restartBtn)


def drawBottomMargin(canvas, data):
    # handles drawing the instructions on the bottom part of the screen
    startY = data.height - data.margin 
    middleY = (startY + data.height)/2
    startX = 10
    buttonSize = 20
    message = """Helpful 
    Keys"""
    canvas.create_text(startX+buttonSize*2, middleY, text=message,
                        fill="gray9", font="Georgia 15")

    spacing = 40
    middleX = data.width/2 - spacing*3
    canvas.create_text(middleX, startY+spacing, text="Press 'r' to restart",
                        fill="gray9", font="Georgia 10")

    canvas.create_text(middleX, data.height-spacing, text="Press 'q' to quit game",
                        fill="gray9", font="Georgia 10")

    middleX = data.width - spacing*6
    canvas.create_text(middleX, data.height-spacing, 
                        text="Press 'p' to pause or un-pause game",
                        fill="gray9", font="Georgia 10")

    canvas.create_text(middleX, startY+spacing, text="Press 'i' for instructions",
                        fill="gray9", font="Georgia 10")


####################################
# use the run function as-is
####################################

def run(rows, cols, width=700, height=650):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        # canvas.update()    
        # the time I rekt Python and my computer and caused a low-level
        # system error :')
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # create the root so images can be loaded
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height

    # this is the hack-y part
    data.rows = rows
    data.cols = cols
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # root.bind("<>")
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()
    # blocks until window is closed
    print("bye!")

run(10, 10, 700, 680)

# you can mess with any of these 4 values and the game should still look alright