from operationscore.PixelEvent import *
class SynchTestEvent(PixelEvent):
    """SynchTestEvent is an event to test the synchronization of the power supplies"""
    def initEvent(self):
        self.eventstate = 0 
        self.cachedDelay = 0
    def state(self, timeDelay):
        if timeDelay != self.cachedDelay:
            self.eventstate += 1 
            self.cachedDelay = timeDelay
        color = [0]*3
        color[self.eventstate % 3] = 255 
        if self.eventstate > 500:
            self.eventstate = 0
        return color
