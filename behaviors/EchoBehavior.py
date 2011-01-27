from operationscore.Behavior import *
import util.Strings as Strings
import pdb
class EchoBehavior(Behavior):
    """EchoBehavior generates a RED response at all locations specified in sensorInputs.  Useful for
    debugging"""
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            outDict = {}
            outDict[Strings.LOCATION] = sensory[Strings.LOCATION]
            outDict['Color'] = (255,0,0) 
            ret.append(outDict)
        return (ret, [])
