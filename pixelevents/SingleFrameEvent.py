from operationscore.PixelEvent import *
class SingleFrameEvent(PixelEvent):
    def initEvent(self):
        self.rendered = False
    def state(self):
        if !self.rendered:
            return self['Color']
        return None
