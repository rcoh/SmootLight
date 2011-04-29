from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class OffScreenDeath(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []

        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()

        for response in sensorInputs:
            opsensory = dict(response)
            
            x = opsensory['Location'][0]
            if x > 0 and x < self.maxX:
                ret.append(opsensory)

        return (ret, []) #no direct ouput
