import time
import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class OneHorizontalInput(Input):
    def inputInit(self):
	self.barCount = 0
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').getSize()
        compReg.getLock().release()
    def sensingLoop(self):
	time.sleep(0.02)
        self.respond({Strings.LOCATION: (self.barCount,0)})
	self.barCount += 1
    def run(self):
	time.sleep(0.1)
        while 1:
            try:
                die = self.parentAlive()
            except:
                break
	    while self.barCount < self.maxX/3:
	        self.acquireLock()
	        self.sensingLoop()
        	self.releaseLock()
 
