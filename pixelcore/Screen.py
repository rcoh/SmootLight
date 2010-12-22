from pixelcore.Pixel import * 
from pixelcore.PixelStrip import *
from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
import util.Search as Search
import util.ComponentRegistry as compReg
import util.Strings as Strings
import itertools
#Class representing a collection of Pixels grouped into PixelStrips.  Needs a
#PixelMapper, currently set via setMapper by may be migrated into the argDict.
class Screen:
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
        self.xSortedPixels = []
        self.xPixelLocs = []
        sizeValid = False 
    def addStrip(self, lS):
        self.pixelStrips.append(lS)
        self.sizeValid = False #keep track of whether or not our screen size has
        #been invalidated by adding more pixels
        self.computeXSortedPixels()
    #Returns (pixelIndex, pixel).  Does a binary search.
    def pixelsInRange(self, minX, maxX):
        minIndex = Search.find_ge(self.xPixelLocs, minX) 
        maxIndex = Search.find_le(self.xPixelLocs, maxX)+1
        return self.xSortedPixels[minIndex:maxIndex]
    def computeXSortedPixels(self):
        for pixel in self:
            self.xSortedPixels.append((pixel.location[0], pixel))
        self.xSortedPixels.sort()
        self.xPixelLocs = [p[0] for p in self.xSortedPixels]
    def render(self, surface):
        [lS.render(surface) for lS in self.pixelStrips]
    def allOn(self):
        [lS.allOn(-1) for lS in self.pixelStrips]
    def __iter__(self): #the iterator of all our pixel strips chained togther
        return itertools.chain(*[strip.__iter__() for strip in \
            self.pixelStrips]) #the * operator breaks the list into args 
    #increment time -- This processes all queued responses.  Responses generated
    #during this period are added to the queue that will be processed on the next
    #time step.
    def timeStep(self):
        tempQueue = list(self.responseQueue)
        self.responseQueue = []
        for response in tempQueue:
            self.processResponse(response)
        [p.invalidateState() for p in self]
    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
    def getSize(self):
        if self.sizeValid:
            return self.size
        (minX, minY, maxX, maxY) = (10**10,10**10,-10**10,-10*10) #TODO: don't
        #be lazy
        for light in self:
            (x,y) = light.location
            
            minX = min(x, minX)
            maxX = max(x, maxX)

            minY = min(y, minY)
            maxY = max(y, maxY)
        self.size = (0,0, maxX, maxY)
        self.sizeValid = True
        return (0, 0, maxX+100, maxY+100) #TODO: cleaner
    #private
    def processResponse(self, responseInfo): #we need to make a new dict for
        #each to prevent interference
        #[strip.respond(dict(responseInfo)) for strip in self.pixelStrips]
        if type(responseInfo) != type(dict()):
            pass
        if 'Mapper' in responseInfo:
            mapper = compReg.getComponent(responseInfo['Mapper']) 
        else:
            mapper = compReg.getComponent(Strings.DEFAULT_MAPPER)
        #if type(mapper) != type(PixelMapper):
        #    raise Exception('No default mapper specified.')
        pixelWeightList = mapper.mapEvent(responseInfo['Location'], self)
        PixelEvent.addPixelEventIfMissing(responseInfo)
        for (pixel, weight) in pixelWeightList: 
            pixel.processInput(responseInfo['PixelEvent'].scale(weight), 0) #TODO: z-index

