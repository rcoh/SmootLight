from operationscore.PixelEvent import *
class SingleFrameEvent(PixelEvent):
    def initEvent(self):
        self.timeState = -1 
    def state(self, timeDelay):
        print 'singlehit'

        if self.timeState == (-1 or timeDelay):
            self.timeState = timeDelay
            return self.Color
        return None
