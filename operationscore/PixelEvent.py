"""PixelEvent is a class defining a light response.  Inheriting classes should define state,
which should return a color, or None if the response is complete.  Consider
requiring a generate event."""
from operationscore.SmootCoreObject import *
import util.ColorOps as color
from numpy import array, zeros

class PixelEvent(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelEvent.params')
        self.coeffs = zeros(3)
        self.initEvent()
        self.scale = 1
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
        time = 0
        # Automatically provided to subclasses.
        coeffs, timeDelay = self.state(time) or (zeros(3), None)
        (c,b,a), self.coeffs = coeffs - self.coeffs, coeffs
        shiftedCoeffs = array([c+time*(b+time*a), b+2*time*a, a])
        return self.scale * shiftedCoeffs, timeDelay

def addPixelEventIfMissing(responseDict):
    if not 'PixelEvent' in responseDict:
        if 'Color' in responseDict:
            color = responseDict['Color']
        else:
            raise Exception('Need Color.  Probably')
        from pixelevents.StepEvent import StepEvent
        responseDict['PixelEvent'] = StepEvent.generate(300, color)
