import pygame
import pandas as pd
from pygame import color
from scipy.spatial import distance_matrix

winHeigh = 700
winWidth = 1200 
win = pygame.display.set_mode((winWidth,winHeigh))

backgroundColor = (0, 0, 0)
textColor = (255, 255, 255)
baseColor = (99, 99, 99)
baseHeigh = 50
baseWidth = 50
roadHeigh = 3
roadWidth = 3
pointsColor = (0, 255, 0)
pointHeigh = 30
pointWidth = 30


class Points():
  
    def __init__(self, x, y, points, speed, path, roadColor, roadLength):
        self.x = x
        self.y = y
        self.points = points
        self.speed = speed
        self.path = path
        self.roadColor = roadColor
        self.roadLength = roadLength

    # drawing the points
    def drawPoints(self):
        base = pygame.Rect(0, 0, baseWidth, baseHeigh)
        base.center = (self.x, self.y)
        pygame.draw.rect(win, baseColor, base)
        for x in self.points:
            rect = pygame.Rect(0, 0, pointWidth, pointHeigh)
            rect.center = (x[0], x[1])
            pygame.draw.rect(win, pointsColor , rect)

    def showDistance(self, distance):
        font = pygame.font.SysFont('Comic Sans MS', 20)
        textsurface = font.render('In a straight line: ' + str(distance), True, textColor)
        win.blit(textsurface,(0.78*winWidth, 0.04*winHeigh))

    def currentNumPixels(self, num):
        font = pygame.font.SysFont('Comic Sans MS', 20)
        textsurface = font.render('Pixels: ' + str(num), True, textColor)
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0.78*winWidth, 0.08*winHeigh, textsurface.get_width(), textsurface.get_height()))
        win.blit(textsurface,(0.78*winWidth, 0.08*winHeigh))

    # changes the color of the path
    def changeColor(self, color):
        self.roadColor = color

    # drawing a path
    def drawPath(self):
        #pygame.draw.circle(win, backgroundColor, (self.x, self.y), roadWidth, roadHeigh)
        if self.x < (self.path[0])[0]:
            self.x += self.speed
            self.roadLength += self.speed
        if self.x > (self.path[0])[0]:
            self.x -= self.speed
            self.roadLength += self.speed
        if self.y < (self.path[0])[1]:
            self.y += self.speed
            self.roadLength += self.speed
        if self.y > (self.path[0])[1]:
            self.y -= self.speed
            self.roadLength += self.speed
        z = (self.x - (self.path[0])[0], self.y - (self.path[0])[1])
        if (z[0] / -self.speed, z[1] / -self.speed) == (0,0):
            self.path = self.path[1:]
        
        pygame.draw.circle(win, self.roadColor, (self.x, self.y), roadWidth, roadHeigh)

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