from operationscore.PixelEvent import *
class SingleFrameEvent(PixelEvent):
    def initEvent(self):
        self.timeState = -1 
    def state(self, timeDelay):
        if self.timeState == -1:
            self.timeState = timeDelay
        if self.timeState == timeDelay:
            return self.Color
        return None
