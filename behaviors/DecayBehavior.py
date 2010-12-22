from operationscore.Behavior import *
from pixelevents.DecayEvent import *
import util.Strings as Strings
import pdb
class DecayBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            outDict = {}
            outDict[Strings.LOCATION] = sensory[Strings.LOCATION]
            outDict['PixelEvent'] = \
            DecayEvent.generate(self['DecayType'],self['Coefficient'], sensory['Color'])
            ret.append(outDict)
        return (ret, recursiveInputs)
