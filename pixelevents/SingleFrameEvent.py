from operationscore.PixelEvent import *
from numpy import array

class SingleFrameEvent(PixelEvent):
    """SingleFrameEvent is a PixelEvent that will only render for the first frame on which it is
    queried"""
    def coeffs(self):
        return array([1., 0., 0.])
