import pygame
from pygame.locals import *

from algorithms import Algorithms
from points import Points

pygame.init()
run = True
pygame.display.set_caption("Symulation")
clock = pygame.time.Clock()
timeTick = 120 #fps
colors = {'red': (255,0,0), 'blue': (0,0,255), 'orange': (255,125,0), 'cyan': (0,255,255)}

    
temp0 = 1000            # start temperature from literature
tempEnd = 0.1           # end temperature
beta = temp0 / 10000    # linear cooling parameter
alpha = 0.95            # geometric cooling parameter

x = 600 # x base
y = 350 # y base
points = [(500,350),(550,250),(20,650),(700,150),(900,250),(800, 600),(30,30)]  #points  
speed = 1 
path = [] 
colorStart = list(colors.keys())[0]

p = Points(x, y, points, speed, path, colorStart, 0)
p.drawPoints()

matrix = p.getMatrixDistances() # destances matrix
numPoints = len(points)+1 # number of points (points + base)
capacity = 2 # load capacity of the trolley
posBase = 0 # base position

alg = Algorithms(matrix, capacity, numPoints, posBase, temp0, tempEnd, beta, alpha, numPoints)

permGreedy = alg.greedyAlg()
distGreedy = round(alg.calculateDistance(permGreedy),2)
print(permGreedy)
print(distGreedy)
permAnnealing = alg.simAnnealing("geo")
print(permAnnealing[1])
print(round(permAnnealing[0],2))
p.setPath(permGreedy)

p.showDistance(distGreedy)


length = len(p.path) - 1
i = 1
while run:
    p.currentNumPixels(p.roadLength)
    if len(p.path) != 0:
        if len(p.path) == length - capacity - 1:
            if len(colors) == i:
                i = 0
            p.changeColor(list(colors.keys())[i])
            length = len(p.path)
            i += 1
        p.drawPath()
    
    for x in pygame.event.get():
        if x.type == QUIT:
            run = False
    clock.tick(timeTick)
    pygame.display.flip()