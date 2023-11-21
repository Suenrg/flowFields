## Bea Shakow, flow fields funcs.py
from p5 import *
import random


class grid:
    def __init__(self, screenSize, extendAmt, resolution, numParticles, stepSize):
        ##
        self.noiseScale = .005
        self.lineCutoff = 30
        ## set up bounds
        self.screenSize = screenSize
        self.left = screenSize.x * extendAmt *  -1 
        self.right = screenSize.x * (1+extendAmt)
        self.top = screenSize.y * extendAmt * -1
        self.bottom = screenSize.y * (1+extendAmt)
        self.resolution = resolution
        ## set up rows and column numbers, as well as square size
        self.numRows = int((self.right - self.left ) / resolution)
        self.numColumns = int((self.bottom - self.top)  / resolution)
        self.squareSize =  screenSize.x /  self.numRows
        
        ## store gridSquares and particles
        self.grid = []
        self.particles = []
        self.stepSize = stepSize

        ## setup grid
        for row in range(self.numRows):
            self.grid.append([])
            for column in range(self.numColumns):
                self.grid[row].append([])
                self.grid[row][column] = gridSquare(self, row, column, self.squareSize, self.numRows) 

        ## spawn particles
        for i in range(numParticles):
            startPos = Vector(random.uniform(0.0, self.screenSize.x), random.uniform(0.0, self.screenSize.y))
            self.particles.append(particle(startPos, self))

    def update(self):
        for i in range(len(self.particles)):
            # if (self.particles[i].alive == True):
            # self.draw()
            self.particles[i].update()

    def draw(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y].draw()

    def findClosestSquare(self, pos):
        x_offset = pos.x - self.left
        y_offset = pos.y - self.top
        columnIndex = int(x_offset / self.resolution)
        rowIndex = int(y_offset / self.resolution)
        return self.grid[columnIndex][rowIndex].angle



class gridSquare:
    def __init__(self, canvas, row, column, squareSize, numRows):

        self.lineLen = .5 * squareSize  # set line len

        temp_x = (row * squareSize) + (.5 * squareSize) #get pos
        temp_y = (column * squareSize) + (.5 * squareSize)
        self.pos = Vector (temp_x, temp_y)

        self.squareSize = squareSize # get squaresize 
        self.angle = angleFunc(canvas, self.pos) # and give myself an angle  

        baseVec = Vector(0 + self.lineLen, 0) ### start with a certain length line at the origin
        baseVec.rotate(self.angle) ### rotate it to the angle we want
        self.angleVec = self.pos + baseVec

        # print(f'pos = {self.pos} , newVec = {newVec}')

    def update():
        # do something here 
        print('nothing here yet')

    def draw(self):
        # print(self)
        circle(self.pos, 5)
        line(self.pos, self.angleVec)

    def __str__(self):
        return(f"X: {self.pos.x}, Y: {self.pos.y}, squaresize = {self.squareSize}, angle= {self.angle}")
    

def angleFunc(canvas, pos):
    noiseVal = noise(pos.x * canvas.noiseScale, pos.y * canvas.noiseScale) * 2 * PI
    return noiseVal

class particle:
    
    def __init__(self, startPos, canvas):
        self.pos = startPos
        self.canvas = canvas
        self.grid = canvas.grid
        self.angle = 0
        self.stepSize = canvas.stepSize
        self.lineList = [self.pos]
        self.alive = True
        red = noise(self.pos.x * canvas.noiseScale, self.pos.y * canvas.noiseScale) * 255
        green = noise(self.pos.x * canvas.noiseScale, self.pos.y * canvas.noiseScale, 100) * 255
        blue = noise(self.pos.x * canvas.noiseScale, self.pos.y * canvas.noiseScale, 300) * 255
        self.color = Color(red, green, blue)

    def update(self):
        ## check if we're in bounds
        self.alive = self.boundsCheck()
        # if len(self.lineList) > self.canvas.lineCutoff:
        #     self.alive = False
        if (self.alive):
            ## find closest Grid Point and set our angle to it
            self.angle = self.canvas.findClosestSquare(self.pos)
            ## calculate steps
            stepX = cos(self.angle)
            stepY = sin(self.angle)
            stepVec = Vector(stepX, stepY).normalize() * self.stepSize

            ## edit position and add it to the line
            self.pos = self.pos + stepVec
            self.lineList.append(self.pos)

            ## check if we're in bounds
            # if (self.boundsCheck()):
                ## draw self
            self.draw()
        else:
            self.draw()

    def draw(self):
        push_style()
        no_fill()
        stroke(self.color)
        begin_shape()
        curve_vertex(self.lineList[0].x, self.lineList[0].y)
        for i in range(len(self.lineList)):
            curve_vertex(self.lineList[i].x, self.lineList[i].y)
        curve_vertex(self.lineList[-1].x, self.lineList[-1].y)
        end_shape()
        pop_style()
    
    def boundsCheck(self):
        x = self.pos.x
        y = self.pos.y

        if x < self.canvas.left:
            startPos = Vector(self.canvas.right - 1, self.pos.y)
            self.canvas.particles.append(particle(startPos, self.canvas))
            return False
        
        if x > self.canvas.right:
            startPos = Vector(self.canvas.left + 1, self.pos.y)
            self.canvas.particles.append(particle(startPos, self.canvas))
            return False

        if y < self.canvas.top:
            startPos = Vector(self.pos.x, self.canvas.bottom - 1)
            self.canvas.particles.append(particle(startPos, self.canvas))
            return False #self.pos.y = self.canvas.bottom - 1

        if y > self.canvas.bottom:
            startPos = Vector(self.pos.x, self.canvas.top + 1)
            self.canvas.particles.append(particle(startPos, self.canvas))
            return False #self.pos.y = self.canvas.top + 1 
        
        return True