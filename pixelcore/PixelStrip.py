from pixelcore.Pixel import *
from pixelevents.StepEvent import *
import pygame
import math
import Util
import pdb
#Python class representing a single Pixel strip (usually 50 Pixels)
class PixelStrip:
    def __init__(self, layoutEngine):
        self.initStrip(layoutEngine)
        self.argDict = layoutEngine.getStripArgs()
    def initStrip(self, layoutEngine):
        pixelLocations = layoutEngine.getPixelLocations()
        self.pixels = [Pixel(l) for l in pixelLocations]
    def __iter__(self):
        return self.pixels.__iter__()
    def render(self, surface):
        [l.render(surface) for l in self.pixels]
        #step
    def allOn(self, time):
        [l.turnOnFor(time) for l in self.pixels] #TODO: add test-on method to
        #pixels
    def respond(self, responseInfo):
        location = responseInfo[Util.location]
        if not 'PixelEvent' in responseInfo:
            if 'Color' in responseInfo:
                color = responseInfo['Color']
            else:
                raise Exception('Need Color.  Probably')
            responseInfo['PixelEvent'] = StepEvent.generate(300, color)
        (dist, pixel) = self.getPixelNearest(location)
        pixel.processInput(responseInfo['PixelEvent'], 0) #TODO: z-index
        
    def getPixelNearest(self, location):
        dists = [(Util.dist(location, pixel.location), pixel) for pixel in self.pixels]
        dists.sort()
        return dists[0]
        #just for now.

