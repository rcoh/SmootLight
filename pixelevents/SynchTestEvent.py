from operationscore.PixelEvent import *
from numpy import array

class SynchTestEvent(PixelEvent):
    """SynchTestEvent is an event to test the synchronization of the power supplies"""
    def initEvent(self):
        self.eventstate = 0
        self.colors = ([200,0,0],[0,200,0],[0,0,200])
    def state(self, time):
        self.Color = self.colors[self.eventstate]
        self.eventstate = (self.eventstate + 1) % 3
        return (array([1.,0.,0.]), time+10)
