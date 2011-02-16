from pixelcore.Pixel import * 
from pixelcore.PixelStrip import *
from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
import util.Search as Search
import util.ComponentRegistry as compReg
import util.Strings as Strings
import util.TimeOps as timeops
import itertools
import sys
import pdb
from logger import main_log
class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips.  Needs a
    PixelMapper, currently set via setMapper by may be migrated into the argDict."""
    
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
        self.xSortedPixels = []
        self.xPixelLocs = []
        sizeValid = False 
        self.pixelsSorted = False 
    
    def addStrip(self, strip):
        self.pixelStrips.append(strip)
        self.sizeValid = False #keep track of whether or not our screen size has
        self.pixelsSorted = False
        #been invalidated by adding more pixels
        
    def pixelsInRange(self, minX, maxX):
        """Returns (pixelIndex, pixel).  Does a binary search.  Sorts first if neccesary."""
        if not self.pixelsSorted:
            self.computeXSortedPixels()
        minIndex = Search.find_ge(self.xPixelLocs, minX) 
        maxIndex = Search.find_le(self.xPixelLocs, maxX)+1
        return self.xSortedPixels[minIndex:maxIndex]
        
    def computeXSortedPixels(self):
        self.xSortedPixels = []
        for pixel in self:
            self.xSortedPixels.append((pixel.location[0], pixel))
        self.xSortedPixels.sort()
        self.xPixelLocs = [p[0] for p in self.xSortedPixels]
        self.pixelsSorted = True 
    
    def __iter__(self): #the iterator of all our pixel strips chained togther
        return itertools.chain(*[strip.__iter__() for strip in \
            self.pixelStrips]) #the * operator breaks the list into args 
            
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
        
    def getSize(self):
        """Returns the size of the screen in the form: (minx, miny, maxx, maxy)"""
        if self.sizeValid:
            return self.size
        (minX, minY, maxX, maxY) = (sys.maxint,sys.maxint,-sys.maxint,-sys.maxint)
        for light in self:
            (x,y) = light.location
            
            minX = min(x, minX)
            maxX = max(x, maxX)

            minY = min(y, minY)
            maxY = max(y, maxY)
        self.size = (0,0, maxX, maxY)
        self.sizeValid = True
        return (minX, minY, maxX, maxY) 
        
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
