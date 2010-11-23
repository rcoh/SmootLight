from Behavior import Behavior
import Util
import pdb
class EchoBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            outDict = {}
            outDict[Util.location] = sensory[Util.location]
            outDict['Color'] = (255,0,0) 
            ret.append(outDict)
        return ret
