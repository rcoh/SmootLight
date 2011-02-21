from operationscore.PixelEvent import *
class SingleFrameEvent(PixelEvent):
    """SingleFrameEvent is a PixelEvent that will only render for the first frame on which it is
    queried"""

    def initEvent(self):
        self.timeState = -1 
    def state(self, timeDelay):
        print timeDelay
        if self.timeState == -1:
            self.timeState = timeDelay
        if self.timeState == timeDelay:
            return self.Color
        return None
