import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
import random
from operationscore.Input import *
class ParametricLocationInput(Input):
    """Takes three arguments: xEquation, yEquation, and useClock where
        xEquation and yEquation is a parametric equation in t and returns
        a value from 0 to 1, where 0 represents top/left and 1 represents
        bottom/right of the lightscreen. useClock is a boolean that 
        specifies if the behavior should compute t based on the system
        clock (value True) or should just increment t every time the
        input is called."""

    def clockTick(self):
        return clock.time() - clock.t

    def callTick(self):
        self.t += 1
        return self.t - 1

    def inputInit(self):
        self.t = 0

        compReg.getLock().acquire()
        xmin, ymin, xmax, ymax = compReg.getComponent('Screen').size
        compReg.getLock().release()

        xlen = xmax-xmin
        ylen = ymax-ymin

        if self['useClock']:
            self.t=self.clock()
            self.getTime = self.clockTick
        else:
            self.t=0
            self.getTime = self.callTick

        self.x_eqn = eval('lambda t:' + str(xmin) + '+' + str(xlen) + '*(' + str(self['xEquation']) + ')')
        self.y_eqn = eval('lambda t:' + str(xmin) + '+' + str(xlen) + '*(' + str(self['yEquation']) + ')')

    def sensingLoop(self):
        self.respond({Strings.LOCATION: (self.x_eqn(self.t), self.y_eqn(self.t))})
        self.t += 1
        
