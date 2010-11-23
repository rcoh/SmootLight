from Light import Light
from PixelStrip import PixelStrip
import itertools
class Screen:
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
    def addStrip(self, lS):
        self.pixelStrips.append(lS)
    def render(self, surface):
        [lS.render(surface) for lS in self.pixelStrips]
    def allOn(self):
        [lS.allOn(-1) for lS in self.pixelStrips]
    def __iter__(self): #the iterator of all our light strips chained togther
        return itertools.chain(*[strip.__iter__() for strip in self.pixelStrips]) 
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
    #private
    def processResponse(self, responseInfo): #we need to make a new dict for
        #each to prevent interference
        [strip.respond(dict(responseInfo)) for strip in self.pixelStrips]

