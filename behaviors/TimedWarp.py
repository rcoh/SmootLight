from operationscore.Behavior import *
from util import Geo
import util.ComponentRegistry as compReg
import pdb

class TimedWarp(Behavior):
    def behaviorInit(self):
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()
 
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for response in sensorInputs:
            opsensory = dict(response)
            if 'FramesToDeath' not in opsensory:
                opsensory['FramesToDeath'] = self['FramesToDeath']
            opsensory['FramesToDeath'] -= 1
            if opsensory['FramesToDeath'] <= 0:
                if opsensory['Direction'] < 0:
                    opsensory['Location'] = (-5, 0)
                else:
                    opsensory['Location'] = (self.maxX + 5, 0)
            ret.append(opsensory)
        return (ret, []) #no direct ouput
