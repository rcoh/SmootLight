import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class ContinuousCenterInput(Input):
    def inputInit(self):
        compReg.getLock().acquire()
        minX,minY,maxX,maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()
        self.center = ((minX+maxX) / 2, (minY+maxY) / 2)
    def sensingLoop(self):
        self.respond({Strings.LOCATION: self.center})
         
