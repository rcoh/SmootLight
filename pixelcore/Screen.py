from pixelcore.Pixel import * 
from pixelcore.PixelStrip import *
import itertools
#Class representing a collection of Pixels grouped into PixelStrips.  Needs a
#PixelMapper, currently set via setMapper by may be migrated into the argDict.
class Screen:
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
        sizeValid = False 
    def addStrip(self, lS):
        self.pixelStrips.append(lS)
        self.sizeValid = False #keep track of whether or not our screen size has
        #been invalidated by adding more pixels
    def render(self, surface):
        [lS.render(surface) for lS in self.pixelStrips]
    def setMapper(self, mapper):
        self.mapper = mapper
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
        self.size = (minX, minY, maxX, maxY)
        self.sizeValid = True
        return (minX, minY, maxX, maxY)
    #private
    def processResponse(self, responseInfo): #we need to make a new dict for
        #each to prevent interference
        #[strip.respond(dict(responseInfo)) for strip in self.pixelStrips]
        if type(responseInfo) != type(dict()):
            pdb.set_trace()
        pixelWeightList = self.mapper.mapEvent(responseInfo['Location'], self)
        Util.addPixelEventIfMissing(responseInfo)
        for (pixel, weight) in pixelWeightList: 
            pixel.processInput(responseInfo['PixelEvent'].scale(weight), 0) #TODO: z-index

