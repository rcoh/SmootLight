from operationscore.PixelEvent import *
from numpy import array

class SynchTestEvent(PixelEvent):
    """SynchTestEvent is an event to test the synchronization of the power supplies"""
    def initEvent(self):
        self.i = 0
    def state(self, time):
        self.i = (self.i + 1) % 2
        return [self.i,0.,0.], time+1
