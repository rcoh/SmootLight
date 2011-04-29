from operationscore.PixelEvent import *
from numpy import array,zeros

class SynchTestEvent(PixelEvent):
    """SynchTestEvent is an event to test the synchronization of the power supplies"""
    def initEvent(self):
        self.i = 0
    def state(self, time):
        self.i = (self.i + 1) % 3
        ret = zeros(3)
        ret[self.i] = 1
        return ret, time+1