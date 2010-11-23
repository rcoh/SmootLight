import Util
import pdb
from StepEvent import StepEvent
#Light keeps a cue of events (LightEvent objects).  Every time is state is
#requested, it processes all the members of its cue.  If a member returns none,
#it is removed from the queue.  Otherwise, its value added to the lights color
#weighted by z-index.
class Light:
    radius = 2
    lightOn = False
    timeOff = -1
    def __init__(self, location, color):
        self.location = location
        self.color = color
        self.events = {}
    def turnOn(self):
        self.lightOn = True
    def turnOnFor(self, time):
        event = StepEvent.generate(time, (255,0,255)) #TODO: Move color to
        self.processInput(event, 0)
        #arg
    def processInput(self,lightEvent,zindex): #consider migrating arg to dict
        self.events[Util.time()] = (zindex, lightEvent)
    def turnOff(self):
        self.lightOn = False
    def lightState(self):
        deadEvents = []
        currentTime = Util.time()
        resultingColor = (0,0,0)
        for eventTime in self.events: #TODO: right color weighting code
            (zindex,event) = self.events[eventTime]
            eventResult = event.lightState(currentTime-eventTime)
            if eventResult != None:
                resultingColor = Util.combineColors(eventResult, resultingColor)
                print resultingColor
            else:
                deadEvents.append(eventTime)
        [self.events.pop(event) for event in deadEvents]
        if sum(resultingColor) > 0:
            print resultingColor
        return tuple(resultingColor)
    def isLightOn(self):
        if self.timeOff == -1:
            return self.lightOn
        else:
            return Util.time() < self.timeOff 
    def flip(self):
        self.lightOn = not self.lightOn
    def __str__(self):
        return 'Loc: ' + str(self.location)

