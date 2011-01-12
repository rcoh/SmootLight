from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Geo as Geo
import util.Strings as Strings
import random
class RandomWalk(Behavior):
    def processResponse(self, sensors, recursives):
        ret = []
        for sensory in sensors:
            s = self['StepSize']
            step = [random.randint(-s,s), random.randint(-s,s)]
            outdict = dict(sensory)
            outdict[Strings.LOCATION] = Geo.addLocations(step, outdict[Strings.LOCATION])
            ret.append(outdict)
        return (ret,recursives)

        
        
