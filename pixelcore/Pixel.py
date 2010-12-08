import Util
import pdb
from pixelevents.StepEvent import *
#Pixel keeps a queue of events (PixelEvent objects) (actually a dictionary
#keyed by event time).  Every time is state is
#requested, it processes all the members of its queue.  If a member returns none,
#it is removed from the queue.  Otherwise, its value added to the Pixels color
#weighted by z-index.
class Pixel:
    radius = 2
    timeOff = -1
    def __init__(self, location):
        self.location = location
        self.events = {}
        self.memState = None
    def turnOn(self):
        self.turnOnFor(-1)
    #Turn the light white for 'time' ms.  Really only meant for testing.  Use
    #processInput instead.  Also, you shouldn't use this anyway.  You should be
    #using the input method on the screen!
    def turnOnFor(self, time):
        event = StepEvent.generate(time, (255,255,255)) #TODO: Move color to
        self.processInput(event, 0)
        #arg
    #Add a pixelEvent to the list of active events
    def processInput(self,pixelEvent,zindex): #consider migrating arg to dict
        self.events[Util.time()] = (zindex, pixelEvent)
    def clearAllEvents(self):
        self.events = {}
    #Combines all PixelEvents currently active and computes the current color of
    #the pixel.
    def invalidateState(self):
        self.memState = None
    def state(self):
        if self.memState != None:
            return self.memState
        if len(self.events) == 0:
            return (0,0,0)
        deadEvents = []
        currentTime = Util.time()
        resultingColor = (0,0,0)
        for eventTime in self.events: #TODO: right color weighting code
            (zindex,event) = self.events[eventTime]
            eventResult = event.state(currentTime-eventTime)
            if eventResult != None:
                resultingColor = Util.combineColors(eventResult, resultingColor)
            else:
                deadEvents.append(eventTime)
        [self.events.pop(event) for event in deadEvents]
        resultingColor = [int(round(c)) for c in resultingColor]
        self.memState = tuple(resultingColor)
        return tuple(resultingColor)
    def __str__(self):
        return 'Loc: ' + str(self.location)

