import math
from operationscore.PixelEvent import *
from util.ColorOps import * 
import util.Geo as Geo
class FadeIn(PixelEvent):
    def state(self, timeDelay):
        decay = math.sin(timeDelay/float(1000))
        if timeDelay > 5000:
            return None
        if timeDelay > 2000 and timeDelay < 4000:
            decay = 1
        return multiplyColor(self.Color,decay)
