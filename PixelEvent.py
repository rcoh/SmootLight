#Class defining a light response.  Inheriting classes should define lightState,
#which should return a color, or None if the response is complete.  Consider
#requiring a generate event.
from SmootCoreObject import SmootCoreObject
class PixelEvent(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelEvent.params')
        self.initEvent()
    def initEvent(self):
        pass
    def lightState(self,timeDelay):
        pass
        
