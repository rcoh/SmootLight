import util.ColorOps as color
import pdb
from pixelevents.StepEvent import *
import util.TimeOps as timeops
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
        self.events = []
        self.lastRenderTime = timeops.time()
        self.lastRender = (0,0,0) 
        
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
    def processInput(self,pixelEvent,zindex, scale=1,currentTime=None): #consider migrating arg to dict
        #TODO: fix for multiple pixel events
        if currentTime == None:
            currentTime = timeops.time()
        #if not currentTime in self.events:
        #    self.events[currentTime] = []
        #self.events[currentTime].append((zindex,scale, pixelEvent))
        self.events.append((currentTime, zindex, scale, pixelEvent)) #TODO: this is kindof
        #gross
    def clearAllEvents(self):
        self.events = [] 
        
    #Combines all PixelEvents currently active and computes the current color of
    #the pixel.
    def state(self, currentTime=timeops.time()): #TODO: this only evaluates at import time, I think
        if currentTime-self.lastRenderTime < 5:
            return self.lastRender
        if self.events == []:
            self.lastRenderTime = currentTime
            return (0,0,0)
        deadEvents = []
        resultingColor = (0,0,0)
        colors = []
        for eventObj in self.events: #TODO: right color weighting code
            if len(self.events) > 50:
                pdb.set_trace()
        #TODO: this sucks.  fix it
            eventTime, zindex, scale, pixelEvent = eventObj
            eventResult = pixelEvent.state(currentTime-eventTime)
            if eventResult != None:
                scaledEvent = color.multiplyColor(eventResult,scale)
                if (scaledEvent[0] + scaledEvent[1] + scaledEvent[2]) < 5:
                    deadEvents.append(eventObj)
                else:
                    colors.append(scaledEvent)
            else:
                deadEvents.append(eventObj)
        
        resultingColor = color.combineColors(colors)
        [self.events.remove(event) for event in deadEvents]
        resultingColor = [int(round(c)) for c in resultingColor]
        self.lastRender = tuple(resultingColor)
        self.lastRenderTime = currentTime
        return tuple(resultingColor)
        
    def __str__(self):
        return 'Loc: ' + str(self.location)

