import pygame
import pandas as pd
from scipy.spatial import distance_matrix
import math
from itertools import groupby


simBackgroundColor = (99, 99, 99)
interBackgroundColor = (0, 0, 0)
textColor = (255, 255, 255)
baseColor = (255, 255, 255)
baseHeigh, baseWidth = 50, 50
roadHeigh, roadWidth = 3, 3
pointsColor = (0, 255, 0)
pointHeigh, pointWidth = 60, 60

winWidth, winHeigh = 1500, 700


PALLET = pygame.transform.scale(pygame.image.load('pallet.png'), (pointWidth, pointHeigh))



class Window():
    
    def __init__(self, x, y, points, speed, d, path, roadColor, win, roadLength=0):
        self.x = x
        self.y = y
        self.points = points
        self.speed = speed
        self.d = d
        self.path = path
        self.roadColor = roadColor
        self.roadLength = roadLength

        self.win = win
        self.winSim = pygame.Surface((0.8*winWidth,winHeigh))
        self.winSim.fill(simBackgroundColor)
        self.winInter = pygame.Surface((0.2*winWidth, winHeigh))
        self.winInter.fill(interBackgroundColor)
        self.win.blit(self.winSim, (0,0))
        self.win.blit(self.winInter, (0.8*winWidth, 0))

    # drawing base
    def drawBase(self):
        base = pygame.Rect(0, 0, baseWidth, baseHeigh)
        base.center = (self.x, self.y)
        pygame.draw.rect(self.win, baseColor, base)

    # drawing the points
    def drawPoints(self):
        num = 1
        for x in self.points:
            font = pygame.font.SysFont('Comic Sans MS', 20)
            text = font.render(str(num), True, (0,0,0))
            rect = PALLET.get_rect()
            rect.center = (x[0], x[1])
            self.win.blit(PALLET, rect)
            self.win.blit(text,(x[0] - 0.4*pointWidth, x[1]))
            num += 1

    def showArrangement(self, permutation, colors):
        i = 0
        font = pygame.font.SysFont('Comic Sans MS', 16)
        title = font.render("Tasks:", True, textColor)
        self.win.blit(title, (self.winSim.get_width() + 20, 250))
        groups = [list(g) for k, g in groupby(permutation, key=lambda x:x!=0) if k]
        for x in groups:
            nr = font.render(str(i+1), True, textColor)
            text = font.render(str(x), True, textColor)
            self.win.blit(nr, (self.winSim.get_width() + 20, 290 + i*text.get_height()))
            pygame.draw.rect(self.win, list(colors.keys())[i % len(colors)], 
                pygame.Rect(self.winSim.get_width() + 60, 290 + (i+0.5)*text.get_height(), 50, 3))
            self.win.blit(text,(self.winSim.get_width() + 150, 290 + i*text.get_height()))
            i += 1


    def showDistance(self, distance):
        font = pygame.font.SysFont('Comic Sans MS', 18)
        textsurface = font.render('Total distance: ' + str(round(distance, 2)), True, textColor)
        self.win.blit(textsurface,(self.winSim.get_width() + 25, 500))

    def currentNumPixels(self, num):
        font = pygame.font.SysFont('Comic Sans MS', 18)
        textsurface = font.render('Distance traveled: ' + str(round(num, 2)), True, textColor)
        pygame.draw.rect(self.win, interBackgroundColor, 
            pygame.Rect(self.winSim.get_width() + 25, 550, textsurface.get_width() + 30, textsurface.get_height()))
        self.win.blit(textsurface,(self.winSim.get_width() + 25, 550))

    # changes the color of the path
    def changeColor(self, color):
        self.roadColor = color

    # drawing a path
    def drawPath(self):
        tempX, tempY = self.x, self.y
        if self.x < (self.path[0])[0]:
            self.x += self.speed
        if self.x > (self.path[0])[0]:
            self.x -= self.speed
        if self.y < (self.path[0])[1]:
            self.y += self.speed * self.d
        if self.y > (self.path[0])[1]:
            self.y -= self.speed * self.d
        
        if abs(self.x - (self.path[0])[0]) < self.speed:
                self.x = (self.path[0])[0]
        if abs(self.y - (self.path[0])[1]) < self.d * self.speed:
                self.y = (self.path[0])[1]
        
        z = (self.x - (self.path[0])[0], self.y - (self.path[0])[1])
        if (z[0] / -self.speed, z[1] / -self.speed) == (0,0) and len(self.path) > 1:
            self.d = abs(self.y - (self.path[1])[1]) / abs(self.x - (self.path[1])[0] + 0.01)
            if self.d > 5:
                self.speed = 1/self.d
            else:
                self.speed = 1
            self.path = self.path[1:]
        
        self.roadLength += math.sqrt(pow(abs(self.x - tempX), 2) + pow(abs(self.y - tempY), 2))
        pygame.draw.circle(self.win, self.roadColor, (self.x, self.y), roadWidth, roadHeigh)
        

    # sets the path based on the permutation fromm algorithm
    def setPath(self, permutation):
        startingPath = [(self.x, self.y)] + self.points
        path = []
        for x in permutation:
            path.append(startingPath[x])
        self.path = path

    # returns a matrix of distances between points
    def getMatrixDistances(self):
        data = [(self.x, self.y)] + self.points
        df = pd.DataFrame(data, columns=['x', 'y'], index=[x for x in range(len(data))])
        matrix = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
        return matrix