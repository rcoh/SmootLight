import time
import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class OneHorizontalInput(Input):
    def inputInit(self):
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()
    def sensingLoop(self):
	time.sleep(0.5)
	if not self.done:
 	    response = []
 	    for i in xrange(self.maxX):
		response.append({Strings.LOCATION: (i,0)})
	    self.respond(response)
	    self.done = True
