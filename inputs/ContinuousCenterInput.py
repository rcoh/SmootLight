import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class ContinuousCenterInput(Input):
    def inputInit(self):
        minX,minY,maxX,maxY = compReg.getComponent('Screen').getSize()
        self.center = ((minX+maxX) / 2, (minY+maxY) / 2)
        print self.center
    def sensingLoop(self):
        self.respond({Strings.LOCATION: self.center})
         
