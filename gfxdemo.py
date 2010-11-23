import os, sys, random, Util
import pygame
import math
from Light import Light
from LightStrip import LightStrip
from LightSystem import LightSystem
from pygame.locals import *
spacing = 4 
vspacing = 12
def dist(l1, l2):
    return math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def colorAdd(c1, c2):
    if(c1 == None):
        return c2
    if(c2 == None):
        return c1
    c = [min(c1[i]+c2[i], 255) for i in range(4)]
    return Color(*c)
pygame.color.add = colorAdd
class BouncyLightSystem(LightSystem):
    def respond(self, responseInfo):
        location = responseInfo['location']
        data = responseInfo['data']
        if(location[0] < 0):
            data = 'right'
        if(location[0] > self.length):
            data = 'left'
        if(data == None):
            data = 'right'
        if data == 'right':
            change = 20
        else:
            change = -20
        responseInfo['location'] = (location[0]+change, location[1])
        responseInfo['data'] = data
        LightSystem.respond(self,responseInfo)
class BouncyLightSystemMultiple(BouncyLightSystem):
    def respondToInput(self, inputDict):
        if sum(inputDict['mouse']) % 2 == 0:
            color = Color('Blue')
        else:
            color = Color('Red')
        LightSystem.respond(self, {'location':inputDict['mouse'],'data': 'right',
            'color': color})
class DyingLightSystem(LightSystem):
    def respond(self, inputDict):
        if 'responsesLeft' in inputDict:
            inputDict['responsesLeft'] -= 1

class ExplodeLightSystem(LightSystem):
    def respond(self, location, data):
        if data['responsesLeft'] != 0:
            data['responsesLeft'] -= 1
            for i in range(data['responsesLeft']):
                LightSystem.respond(self, (location[0]+random.randint(-50,50),
                    location[1]+random.randint(-5,5)), dict(data))
    def respondToInput(self, inputDict):
        LightSystem.respond(self, inputDict['mouse'], {'responsesLeft':5})
pygame.init()
screen = pygame.display.set_mode((1300,50))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(Color('Black'))
clock = pygame.time.Clock()
l = BouncyLightSystemMultiple(1300, 50)
#l.respond((0, 25), None)
#l.allOn()
while 1:
    for event in pygame.event.get():
        if event.type is MOUSEBUTTONDOWN:
            l.respondToInput({'mouse': pygame.mouse.get_pos()})
    clock.tick(10)
    background.fill(Color('Black'))
    l.render(background)

    screen.blit(background, (0,0))
    pygame.display.flip()
    l.timeStep()




