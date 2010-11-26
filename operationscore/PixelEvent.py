#Class defining a light response.  Inheriting classes should define lightState,
#which should return a color, or None if the response is complete.  Consider
#requiring a generate event.
from operationscore.SmootCoreObject import *
class PixelEvent(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelEvent.params')
        self.initEvent()
    def initEvent(self):
        pass
    def scale(c):
        self['Color'] *= c
    def state(self,timeDelay):
        pass
        
