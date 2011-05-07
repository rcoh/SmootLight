from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class Curtain (Behavior):
    """Curtain is a transition behavior that can only work with functionmap
    animations: it take a functionmap location string and append a multiplying
    coefficient function. 
    <Args>
        <Center> # start of wipeout location, 0 is far left, 1 is far right
        <tEquation> # t valued function that will return at what distance
            light will be cut off/resume
        # defaults are .5 and t/90.0    
        """
    
    def behaviorInit (self):
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
            self.tEq = lambda t: t / 90.0
        return [0]

    def processResponse (self, inputs, state):

        #step = lambda x: ((numpy.sign(x)+1)/2)
        #cutoff = tEquation(t) * self.scrwid
        ##takes a location and returns distance from center
        #mapper = lambda loc: abs(loc - center)
        #curtain = lambda x: step(mapper(x) - cutoff)

        locmask = "((numpy.sign(numpy.abs(x - " + str(self.center) + ") - " \
            + str(self.tEq(state[0]) * self.scrwid / 2) + ")+1)/2)"

        #print "Curtain locmask:", locmask

        for inp in inputs:
             inp['Location'] = "(" + inp['Location'] + ") * " + locmask

        return (inputs, [state[0]+1])
