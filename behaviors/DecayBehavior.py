from operationscore.Behavior import *
from pixelevents.DecayEvent import *
import Util
import pdb
class DecayBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        #TODO: move into params
        for sensory in sensorInputs:
            outDict = {}
            outDict[Util.location] = sensory[Util.location]
            outDict['PixelEvent'] = \
            DecayEvent.generate('Proportional',100, sensory['Color'])
            ret.append(outDict)
        return ret
