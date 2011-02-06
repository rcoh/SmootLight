from operationscore.PixelEvent import *
import math
from util.ColorOps import * 
import random
class RandomEvent(PixelEvent):
    def initEvent(self):
        self.timeState = -1 
    def state(self, timeDelay):
        if self.timeState == -1:
            self.timeState = timeDelay
        if self.timeState == timeDelay:
            return multiplyColor(self.Color, random.random())
        return None
