import time
import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class LeftEdgeInput(Input):
    def inputInit(self):
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').getSize()
        compReg.getLock().release()
    def sensingLoop(self):
    	time.sleep(0.5)
    	if not self.done:
            response = []
            response.append({Strings.LOCATION: (self.minX+5,25)}) #Y set to 25 so that BQS detects
            self.respond(response)
            self.done = True
