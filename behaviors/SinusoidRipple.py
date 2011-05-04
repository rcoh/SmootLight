from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import math

class SinusoidRipple (Behavior):
    """SinusoidRipple makes a ripple effect about a center.
    <Args>
        <Center> # by default, .5
        <tEquation> # by default, 30*math.cos(t/(30*2*math.pi))
    """

    def behaviorInit(self):
        self.xMin, self.yMin, self.xMax, self.yMax = \
                                        compReg.getComponent('Screen').size
        self.scrwid = self.xMax - self.xMin
        
        if 'Center' in self.argDict:
            self.center = self['Center'] * self.scrwid
        else:
            self.center = .5 * self.scrwid
        if 'tEquation' in self.argDict:
            self.tEq = eval("lambda t: " + self['tEquation'])
        else:
            self.tEq = lambda t: 300 * math.sin((2 * math.pi * t)/300)
        return [0]

    def processResponse (self, inputs, state):

        if not state:
            state = [0] 

        print "SinusoidRipple", inputs, state
        mapper = lambda loc: abs(loc - center)
        scale = self.tEq(state[0]) / (self.scrwid * 2 * math.pi)
        curtain = lambda x: numpy.sin(mapper(x)*scale)

        location = "numpy.abs(numpy.sin(numpy.abs(x - " + str(self.center) + \
            ") * " + str((2*math.pi*self.tEq(state[0])) / self.scrwid) + "))"

        print location
        
        for inp in inputs:
            inp['Location'] = location

        return (inputs, [state[0]+1])
