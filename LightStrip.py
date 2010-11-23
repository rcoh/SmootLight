from Light import Light
from StepEvent import StepEvent
import pygame
import math
import Util
import pdb
#Python class representing a single light strip (usually 50 lights)
class PixelStrip:
    def __init__(self, layoutEngine):
        self.initStrip(layoutEngine)
        self.argDict = layoutEngine.getStripArgs()
    def initStrip(self, layoutEngine):
        lightLocations = layoutEngine.getLightLocations()
        self.lights = [Light(l, (0,0,0)) for l in lightLocations]
    def __iter__(self):
        return self.lights.__iter__()
    def render(self, surface):
        [l.render(surface) for l in self.lights]
        #step
    def allOn(self, time):
        [l.turnOnFor(time) for l in self.lights]
    def turnOnLight(self,light, dist):
        if(dist < 12):
            light.turnOnFor(300)
    def respond(self, responseInfo):
        print 'PixelEvent', responseInfo 
        location = responseInfo[Util.location]
        if not 'PixelEvent' in responseInfo:
            if 'Color' in responseInfo:
                color = responseInfo['Color']
            else:
                raise Exception('Need Color.  Probably')
        responseInfo['PixelEvent'] = StepEvent.generate(300, color)
        (dist, light) = self.getLightNearest(location)
        light.processInput(responseInfo['PixelEvent'], 0) #TODO: z-index
        
    def getLightNearest(self, location):
        dists = [(Util.dist(location, light.location), light) for light in self.lights]
        dists.sort()
        return dists[0]
        #just for now.

