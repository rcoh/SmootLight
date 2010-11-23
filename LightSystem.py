from Light import Light
from LightStrip import LightStrip
import itertools
class Screen:
    def __init__(self):
        self.responseQueue = []
        self.lightStrips = []
    def addStrip(self, lS):
        self.lightStrips.append(lS)
    def render(self, surface):
        [lS.render(surface) for lS in self.lightStrips]
    def allOn(self):
        [lS.allOn(-1) for lS in self.lightStrips]
    #increment time -- This processes all queued responses.  Responses generated
    #during this period are added to the queue that will be processed on the next
    #time step.
    def __iter__(self): #the iterator of all our light strips chained togther
        return itertools.chain(*[strip.__iter__() for strip in self.lightStrips]) 
    def timeStep(self):
        tempQueue = list(self.responseQueue)
        self.responseQueue = []
        for response in tempQueue:
            self.processResponse(response)
    def respond(self, responseInfo):
        print responseInfo
        self.responseQueue.append(responseInfo)
    def processResponse(self, responseInfo): #we need to make a new dict for
        #each to prevent interference
        [strip.respond(dict(responseInfo)) for strip in self.lightStrips]

