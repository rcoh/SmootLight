from operationscore.Behavior import *
import math
class CappedAccelerate(Behavior):
    def behaviorInit(self):
        if self['MaxVelocity'] != None:
            self.maxVelocity = self['MaxVelocity']
        else:
            self.maxVelocity = 20 

        if self['Acceleration'] != None:
            self.accel = self['Acceleration']
        else:
            self.accel = 1.1

    def processResponse(self, sensorInputs, recursiveInputs):

        ret = []

        for sensory in sensorInputs:
            opsensory = dict(sensory)
            opsensory['XStep'] = min(self.maxVelocity, self.accel * opsensory['XStep'])
            ret.append(opsensory)

        return (ret, [])

