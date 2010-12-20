from operationscore.Behavior import *
import util.Strings as Strings
import Util
import pdb
class EchoBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            outDict = {}
            outDict[Strings.LOCATION] = sensory[Strings.LOCATION]
            outDict['Color'] = (255,0,0) 
            ret.append(outDict)
        return ret
