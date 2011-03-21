from pixelcore.Pixel import * 
from pixelcore.PixelStrip import *
from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
import util.ComponentRegistry as compReg
import util.Strings as Strings
import util.TimeOps as timeops
import itertools
import pdb
import numpy
from logger import main_log
import time

class DummyPixelStrip: # to be removed as soon as the rest of the code allows
    def __init__(self, pixels, argDict):
        self.pixels = pixels
        self.argDict = argDict
    def __iter__(self):
        return iter(self.pixels)

class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips.  Needs a
    PixelMapper, currently set via setMapper but may be migrated into the argDict."""
    
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
    
    def initStrips(self, layouts):
        stripLocs = [l.layoutFunc() for l in layouts]
        pixels = [map(Pixel, s) for s in stripLocs]
        for p, l in zip(pixels, layouts):
            self.pixelStrips.append(DummyPixelStrip(p, l.argDict))
        self.locs = numpy.concatenate(stripLocs) # locs is an n-by-2 array of all pixel locations
        self.pixels = numpy.concatenate(pixels)
        self.size = [f(self.locs[:,xy]) for f in (min,max) for xy in (0,1)] # (minX, minY, maxX, maxY)
    
    def pixelsInRange(self, minX, maxX):
        """Returns (pixelIndex, pixel)."""
        index = (minX <= self.locs[:,0]) & (self.locs[:,0] <= maxX)
        return itertools.izip(self.locs[index,0], self.pixels[index])
    
    def __iter__(self): # iterator over all pixels
        return iter(self.pixels)
    
    #SUBVERTING DESIGN FOR EFFICIENCY 1/24/11, RCOH -- It would be cleaner to store the time on the responses
    #themselves, however, it is faster to just pass it in.
    def timeStep(self, currentTime=None):
        """Increments time -- This processes all queued responses, adding that to a queue that will
        be processed on the next time step."""
        if currentTime == None:
            currentTime = timeops.time()
        tempQueue = list(self.responseQueue)
        self.responseQueue = []
        for response in tempQueue:
            self.processResponse(response, currentTime)
        
    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
        
    # depricated: just use self.size
    def getSize(self):
        return self.size
        
    #private
    def processResponse(self, responseInfo, currentTime=None): #we need to make a new dict for
        #each to prevent interference
        if currentTime == None:
            currentTime = timeops.time()
        if type(responseInfo) != type(dict()):
            pass
        if 'Mapper' in responseInfo:
            mapper = compReg.getComponent(responseInfo['Mapper']) 
        else:
            mapper = compReg.getComponent(Strings.DEFAULT_MAPPER)
        pixelWeightList = mapper.mapEvent(responseInfo['Location'], self)
        main_log.debug('Screen processing response.  ' + str(len(pixelWeightList)) + ' events\
generated')
        PixelEvent.addPixelEventIfMissing(responseInfo)
        for (pixel, weight) in pixelWeightList: 
            pixel.processInput(responseInfo['PixelEvent'], 0,weight, currentTime) #TODO: z-index
