import Util
import pdb
from pixelevents.StepEvent import *
#Pixel keeps a queue of events (PixelEvent objects) (actually a dictionary
#keyed by event time).  Every time is state is
#requested, it processes all the members of its cue.  If a member returns none,
#it is removed from the queue.  Otherwise, its value added to the Pixels color
#weighted by z-index.
class Pixel:
    radius = 2
    timeOff = -1
    def __init__(self, location, color):
        self.location = location
        self.color = color
        self.events = {}
    def turnOn(self):
        self.turnOnFor(-1)
    def turnOnFor(self, time):
        event = StepEvent.generate(time, (255,0,255)) #TODO: Move color to
        self.processInput(event, 0)
        #arg
    def processInput(self,pixelEvent,zindex): #consider migrating arg to dict
        self.events[Util.time()] = (zindex, pixelEvent)
    def clearAllEvents(self):
        self.events = {}
    def state(self):
        deadEvents = []
        currentTime = Util.time()
        resultingColor = (0,0,0)
        for eventTime in self.events: #TODO: right color weighting code
            (zindex,event) = self.events[eventTime]
            eventResult = event.state(currentTime-eventTime)
            if eventResult != None:
                resultingColor = Util.combineColors(eventResult, resultingColor)
                print resultingColor
            else:
                deadEvents.append(eventTime)
        [self.events.pop(event) for event in deadEvents]
        if sum(resultingColor) > 0:
            print resultingColor
        return tuple(resultingColor)
    def __str__(self):
        return 'Loc: ' + str(self.location)

