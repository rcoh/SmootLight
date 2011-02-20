import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class ParametricLocationInput(Input):
    '''Continuously returns one of nine positions on the screen as specified by the xloc
    and yloc arguments, which can take values 'min', 'max', and 'center'. '''

    def clockTick(self):
        return clock.time() - clock.t

    def callTick(self):
        self.t += 1
        return self.t - 1

    def inputInit(self):
        self.t = 0

        compReg.getLock().acquire()
        xmin, ymin, xmax, ymax = compReg.getComponent('Screen').getSize()
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
        
