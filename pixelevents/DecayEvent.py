from operationscore.PixelEvent import *
import math
from util.ColorOps import * 
import util.Geo as Geo
from numpy import array, exp

class DecayEvent(PixelEvent):
    """DecayEvent is a pixel event that can decay either Exponentially or Proportionally.  Specify:
    <Coefficient> -- Controls the speed of decay."""

    def initEvent(self):
        self.coeff = float(abs(self.Coefficient))
    def state(self, time):
        if time == 0: return [1, -self.coeff, 0], 1./self.coeff
        return None
    
    @staticmethod
    def generate(decayType, coeff, color):
        args = {'DecayType':decayType, 'Coefficient':coeff, 'Color':color}
        return DecayEvent(args)
