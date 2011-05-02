from operationscore.Behavior import *
import math
class CappedAccelerate(Behavior):

    def processResponse(self, sensorInputs, recursiveInputs):

        ret = []

        if self['MaxVelocity'] != None:
            maxVelocity = self['MaxVelocity']
        else:
            maxVelocity = 20 
        if self['Acceleration'] != None:
            accel = self['Acceleration']
        else:
            accel = 1.1
 
        for sensory in sensorInputs:
            opsensory = dict(sensory)
            opsensory['XStep'] = min(maxVelocity, accel * opsensory['XStep'])
            ret.append(opsensory)

        return (ret, [])

