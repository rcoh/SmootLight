"""PixelEvent is a class defining a light response.  Inheriting classes should define state,
which should return a color, or None if the response is complete.  Consider
requiring a generate event."""
from operationscore.SmootCoreObject import *
import util.ColorOps as color
import numpy

class PixelEvent(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelEvent.params')
        self.coeffs = numpy.zeros(3)
        self.initEvent()
    def initEvent(self):
        pass
    #Returns  a new PixelEvent, but with a response scaled by c.
    def scale(self,c):
        if c == 1:
            return self
        newDict = dict(self.argDict) 
        newDict['Color'] = color.multiplyColor(newDict['Color'], c)
        return self.__class__(newDict)
    def state(self, time):
        """Should return (coeffs, timeDelay).  coeffs are the
        coefficients of a quadratic polynomial in time, lowest degree
        first, such that p(t) is the desired intensity at time t.
        timeDelay specifies when this method should be called again
        (i.e. for how long the polynomial is valid).  If the event is
        finished executing, None should be returned instead of the
        tuple.  All times are relative to the event's creation
        time."""
        raise NotImplementedError
    def changeInState(self, time):
        # Automatically provided to subclasses.
        coeffs, timeDelay = self.state(time) or (0, None)
        (c,b,a), self.coeffs = coeffs - self.coeffs, coeffs
        shiftedCoeffs = [c+time*(b+time*a), b+2*time*a, a]
        return shiftedCoeffs, timeDelay

def addPixelEventIfMissing(responseDict):
    if not 'PixelEvent' in responseDict:
        if 'Color' in responseDict:
            color = responseDict['Color']
        else:
            raise Exception('Need Color.  Probably')
        from pixelevents.StepEvent import StepEvent
        responseDict['PixelEvent'] = StepEvent.generate(300, color)
