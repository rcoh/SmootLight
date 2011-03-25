from operationscore.PixelEvent import *
import math
from util.ColorOps import * 
import util.Geo as Geo
from numpy import array, exp

class DecayEvent(PixelEvent):
    """DecayEvent is a pixel event that can decay either Exponentially or Proportionally.  Specify:
    <DecayType> -- Exponential or Proportional
    <Coefficient> -- Controls the speed of decay."""

    def initEvent(self):
        self.coefficient = float(abs(self.Coefficient))
        if self.DecayType == 'Exponential':
            self.decayType = 1
        else:
            self.decayType = 2
        self.color = self.Color   
    
    def state(self, time):
        # todo: exponential
        if time == 0: return [1, -self.coefficient, 0], self.coefficient
        else: return None
    
    @staticmethod
    def generate(decayType, coefficient, color):
        args = {'DecayType': decayType, 'Coefficient':coefficient, 'Color':color}
        return DecayEvent(args)
    
