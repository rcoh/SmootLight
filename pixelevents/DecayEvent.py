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
        
    #SUBVERTING DESIGN FOR THE SAKE OF EFFICIENCY -- RUSSELL COHEN (2011-01-03-23:18)    
    def state(self,timeDelay):
        if self.decayType == 1:
            decay = Geo.approxexp(timeDelay*-1*self.coefficient)
        if self.decayType == 2:
            decay = self.coefficient / timeDelay # I don't think this does what you want...
        color = multiplyColor(self.color, decay)
        return color if (color[0] + color[1] + color[2]) > 5 else None
    
    def coeffs(self):
        if self.decayType == 1: # exp
            return array([1., exp(-self.coefficient/30), 0.])
        else:
            return array([1., 0., -self.coefficient/30])
    
    @staticmethod
    def generate(decayType, coefficient, color):
        args = {'DecayType': decayType, 'Coefficient':coefficient, 'Color':color}
        return DecayEvent(args)
