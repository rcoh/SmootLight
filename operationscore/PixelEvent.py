#Class defining a light response.  Inheriting classes should define lightState,
#which should return a color, or None if the response is complete.  Consider
#requiring a generate event.
from operationscore.SmootCoreObject import *
from pixelevents.StepEvent import *
import util.ColorOps as color
class PixelEvent(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelEvent.params')
        self.initEvent()
    def initEvent(self):
        pass
    #Returns  a new PixelEvent, but with a response scaled by c.
    def scale(self,c):
        if c == 1:
            return self
        newDict = dict(self.argDict) 
        newDict['Color'] = color.multiplyColor(newDict['Color'], c)
        return self.__class__(newDict)
    def state(self,timeDelay):
        pass
    @staticmethod 
    def addPixelEventIfMissing(responseDict):
        if not 'PixelEvent' in responseDict:
            if 'Color' in responseDict:
                color = responseDict['Color']
            else:
                raise Exception('Need Color.  Probably')
            responseDict['PixelEvent'] = StepEvent.generate(300, color)
        
