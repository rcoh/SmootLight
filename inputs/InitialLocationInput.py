import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
import time
from operationscore.Input import *
class InitialLocationInput(Input):
    """Takes two arguments: xPos, yPos, where xPos and yPos is a value from 
    0 to 1, where 0 represents top/left and 1 represents bottom/right of the
    lightscreen. Will return that position on the screen only once."""

    def inputInit(self):
        compReg.getLock().acquire()
        xmin, ymin, xmax, ymax = compReg.getComponent('Screen').size
        compReg.getLock().release()

        xlen = xmax-xmin
        ylen = ymax-ymin

        self.xloc = xmin + xlen * self['xPos']
        self.yloc = ymin + ylen * self['yPos']

    def sensingLoop(self):
        time.sleep(.5) # Hackery to make sure that things are actually ready
        self.respond({Strings.LOCATION: (self.xloc, self.yloc)})
        self.done = True
        
