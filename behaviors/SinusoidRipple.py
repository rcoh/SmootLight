from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import math

class SinusoidRipple (Behavior):
    """SinusoidRipple makes a ripple effect about a center.
    <Args>
        <Center> # by default, .5, but can also be an equaton in t
        <Scale>  # by default, 30*math.cos(t/(30*2*math.pi))
    """

    def behaviorInit(self):
        self.xMin, self.yMin, self.xMax, self.yMax = \
                                        compReg.getComponent('Screen').size
        self.scrwid = self.xMax - self.xMin
        
        if 'Center' in self.argDict:
            if not isinstance(self['Center'], str):
                self['Center'] = str(self['Center'])
            self.center = eval("lambda t:" + self['Center'] + " * " + \
                                str(self.scrwid))
        else:
            self.center = lambda t:.5 * self.scrwid
        if 'Scale' in self.argDict:
            if not isinstance(self['Scale'], str):
                self['Scale'] = str(self['Scale'])
            self.scale = eval("lambda t: " + self['Scale'])
        else:
            self.scale = lambda t: 100 * math.sin((2 * math.pi * t)/10000)
        return [0]

    def processResponse (self, inputs, state):

        if not state:
            state = [0] 

        #print "SinusoidRipple", inputs, state
        #mapper = lambda loc: abs(loc - center)
        #scale = self.scale(state[0]) / (self.scrwid * 2 * math.pi)
        #curtain = lambda x: numpy.sin(mapper(x)*scale)

        location = "(numpy.sin(numpy.abs(x - " + str(self.center(state[0])) + \
            ") * " + str((2*math.pi*self.scale(state[0])) / self.scrwid) + "))"

        #print location
        
        for inp in inputs:
            inp['Location'] = location

        return (inputs, [state[0]+1])
