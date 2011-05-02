from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class OffScreenDeath(Behavior):
    def behaviorInit(self):
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []


        for response in sensorInputs:
            opsensory = dict(response)
            
            x = opsensory['Location'][0]
            if x > 0 and x < self.maxX:
                ret.append(opsensory)
                print 'xloc:', x
        return (ret, []) #no direct ouput
