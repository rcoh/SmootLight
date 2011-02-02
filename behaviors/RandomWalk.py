from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Geo as Geo
import util.Strings as Strings
import random
import pdb
class RandomWalk(Behavior):
    """Behavior to move the curent location by a random distance specified by 
    <StepSize> -- StepSize in units/response"""

    def processResponse(self, sensors, recursives):
        ret = []
        s = self['StepSize']
        for sensory in sensors:
            step = [random.randint(-s,s), random.randint(-s,s)]
            outdict = dict(sensory)
            outdict[Strings.LOCATION] = Geo.addLocations(step, outdict[Strings.LOCATION])
            ret.append(outdict)
        return (ret,recursives)

        
        
