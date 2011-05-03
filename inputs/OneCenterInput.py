import time
import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class OneCenterInput(Input):
    def inputInit(self):
	self.isRun = False
        compReg.getLock().acquire()
        minX,minY,maxX,maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()
        self.center = ((minX+maxX) / 2, (minY+maxY) / 2)
    def sensingLoop(self):
        self.respond({Strings.LOCATION: self.center})
	self.isRun = True
    def run(self):
	time.sleep(1)
        while 1:
            try:
                die = self.parentAlive()
            except:
                break
	    while not self.isRun:
	        self.acquireLock()
	        self.sensingLoop()
        	self.releaseLock()
 
