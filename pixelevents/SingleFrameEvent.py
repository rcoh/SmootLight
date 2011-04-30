from operationscore.PixelEvent import *
from numpy import array

class SingleFrameEvent(PixelEvent):
    """SingleFrameEvent is a PixelEvent that will only render for the first frame on which it is
    queried"""
    def state(self, time):
        if time == 0: return [1, 0, 0], 1 # wait 1 ms
        return None
