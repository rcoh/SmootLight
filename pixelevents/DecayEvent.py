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
    
    def coeffs(self):
        if self.decayType == 1: # exp
            return (array([1., exp(-self.coefficient/30), 0.]), None)
        else:
            return (array([1., 0., -self.coefficient/30]), None)
    
    @staticmethod
    def generate(decayType, coefficient, color):
        args = {'DecayType': decayType, 'Coefficient':coefficient, 'Color':color}
        return DecayEvent(args)
