## Flow Fields.py

import os
import sys
import random
from p5 import *
from flowFieldsFuncs import *

## Variables
screenSize = Vector(800,800)
resolution = 1/15 * screenSize.x
extendAmt = 0 #.25
default_angle = PI * 0.25
numParticles = 150
bgColor = Color(255,155,86)
fr = 60
stepSize = screenSize.x * .05

canvas = grid(screenSize, extendAmt, resolution, numParticles, stepSize)



def setup():
    size(screenSize.x, screenSize.y)
    # background(bgColor)
    fill(0)
    stroke(1,1,1)
    strokeWeight(3)#4)
    stroke_join('ROUND')
    # for x in range(len(grid)):
    #     for y in range(len(grid[0])):
    #         # print(f"Row {x}, column {y} has a value {grid[0][1]}")

def draw():
    background(bgColor)
    
    fill(0)
    canvas.update()
    # no_loop()


run(renderer="vispy",frame_rate=fr)