from operationscore.PixelEvent import *
import math
from util.ColorOps import * 
class DecayEvent(PixelEvent):
    def initEvent(self):
        self['Coefficient'] = abs(self['Coefficient'])
    def state(self,timeDelay): #TODO: make this fast.
        if self['DecayType'] == 'Exponential':
            decay = math.exp(timeDelay*-1*self['Coefficient'])
        if self['DecayType'] == 'Proportional':
            decay = float(self['Coefficient']) / timeDelay
        color = multiplyColor(self['Color'], decay)
        return color if sum(color) > 5 else None
    @staticmethod
    def generate(decayType, coefficient, color):
        args = {'DecayType': decayType, 'Coefficient':coefficient, 'Color':color}
        return DecayEvent(args)
