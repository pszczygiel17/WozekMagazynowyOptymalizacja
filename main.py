import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

pygame.init()

from algorithms import Algorithms
from window import Window

colors = {'red': (255,0,0), 'blue': (0,0,255), 'orange': (255,125,0), 'cyan': (0,255,255), 
    'yellow': (255,255,0), 'green': (0,255,0), 'violet': (255,0,255), 'pink': (255,153,204)}

PALLET = pygame.transform.scale(pygame.image.load('pallet.png'), (60, 60))

win = pygame.display.set_mode((1500,700))

slider = Slider(win, 1330, 660, 150, 20, min=1, max=5, step=1, handleColour=(90,90,90), handleRadius=9, initial=2)
font = pygame.font.SysFont('Comic Sans MS', 16)
sliderCap = font.render("Cap: " + str(slider.getValue()), True, (255,255,255))

isActive = False
points = []

def setText(s):
    return font.render(s, True, (0,0,0))

btnStartRestart = Button(
        win,  
        1210,  
        600,  
        80, 
        40,  
        text="Start",
        fontSize=20, 
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),  
        pressedColour=(0, 200, 20), 
        radius=20,  
        onClick=lambda: startRestart()
    )
btnStartRestart.disable()
btnStartRestart.text = setText("Start")
btnSet = Button(
        win,
        1320,
        600,
        80,
        40,
        text="Set",
        fontSize=20,
        textColour=(0,0,0),
        inactiveColour=(200, 50, 0), 
        hoverColour=(150, 0, 0),  
        pressedColour=(0, 200, 20), 
        radius=20,  
        onClick=lambda: set()
    )
btnSet.text = setText("Set")
btnSave = Button(
        win,
        1410,
        600,
        80,
        40,
        text="Accept",
        fontSize=20,
        textColour=(0,0,0),
        inactiveColour=(200, 50, 0), 
        hoverColour=(150, 0, 0),  
        pressedColour=(0, 200, 20), 
        radius=20,  
    )
btnSave.text = setText("Accept")

def drawPoint(x, y, num):
    font = pygame.font.SysFont('Comic Sans MS', 20)
    text = font.render(str(num), True, (0,0,0))
    rect = PALLET.get_rect()
    rect.center = (x, y)
    win.blit(PALLET, rect)
    win.blit(text,(x-24, y))

def showOrders():
    font = pygame.font.SysFont('Comic Sans MS', 16)
    title = font.render("Order list:", True, (255,255,255))
    win.blit(title, (1220, 10))
    for x in range(len(points)):
        text = font.render(str(x+1) + "    " + str(points[x]), True, (255,255,255))
        if x < 8:
            win.blit(text, (1220, 50 + x*text.get_height()))
        else:
            win.blit(text, (1370, 50 + (x-8)*text.get_height()))

def startRestart():
    changeState()
    main()

def set():
    run = True
    num = 1
    while run:
        pygame_widgets.update(pygame.event.get())
        for event in pygame.event.get():
            if btnSave.clicked:
                showOrders()
                run = False
                btnStartRestart.enable()
                btnSet.disable()
                break
            if event.type == MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    posX = pygame.mouse.get_pos()[0]
                    posY = pygame.mouse.get_pos()[1]
                    if posX < 1170 and posX > 30 and posY > 30 and posY < 670:
                        x, y = pygame.mouse.get_pos()
                        points.append((x,y))
                        drawPoint(x, y, num)
                        pygame.display.update()
                        num += 1
            if event.type == QUIT:
                exit()

def changeState():
    global isActive, points
    if isActive:
        isActive = False
        points = []
        btnStartRestart.text = setText("Start")
        btnStartRestart.disable()
        btnSet.enable()
        btnStartRestart.setInactiveColour((200, 50, 0))
    else:
        btnStartRestart.text = setText("Reset")
        isActive = True
        btnStartRestart.setInactiveColour((0,200,20))

    
def main():
    global points, sliderCap
    pygame.display.set_caption("Symulation")
    clock = pygame.time.Clock()
    timeTick = 120 #fps
    
    x = 600 # x base
    y = 350 # y base
    
    speed = 1
    d = 1 
    path = [] 
    colorStart = list(colors.keys())[0]
    
    p = Window(x, y, points, speed, d, path, colorStart, win)
    p.drawBase()
    
    if isActive:
        showOrders()
        p.drawPoints()
        matrix = p.getMatrixDistances() # destances matrix
        numPoints = len(points)+1 # number of points (points + base)
        capacity = slider.getValue() # load capacity of the trolley
        posBase = 0 # base position

        alg = Algorithms(matrix, capacity, numPoints, posBase)

        permAnnealing = alg.simAnnealing()
        print(permAnnealing[1])
        print(round(permAnnealing[0],2))

        p.setPath(permAnnealing[1])
        p.showDistance(permAnnealing[0])
        p.showArrangement(permAnnealing[1], colors, alg)

        length = len(p.path) - 1
        i = 1

    while True:
        if isActive:
            if abs(p.roadLength - permAnnealing[0]) < 5:
                p.currentNumPixels(permAnnealing[0])
            else:
                p.currentNumPixels(p.roadLength)
            if len(p.path) != 0:
                if len(p.path) == length - capacity - 1:
                    if len(colors) == i:
                        i = 0
                    p.changeColor(list(colors.keys())[i])
                    length = len(p.path)
                    i += 1
                p.drawPath()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        pygame.draw.rect(win, (0,0,0), pygame.Rect(1220, 660, sliderCap.get_width(), sliderCap.get_height()))
        sliderCap = font.render("Capacity: " + str(slider.getValue()), True, (255,255,255))
        win.blit(sliderCap, (1220, 660))

        pygame_widgets.update(pygame.event.get())

        clock.tick(timeTick)
        pygame.display.update()


if __name__ == "__main__":
    main()