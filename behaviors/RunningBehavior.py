from operationscore.Behavior import *
import pdb
import Util
class RunningBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        newResponses = sensorInputs 
        ret = []
        ret += newResponses
        for recurInput in recursiveInputs:
            outDict = dict(recurInput)
            if not 'Dir' in outDict:
                outDict['Dir'] = 1 #to the right
            outDict['Location']= Util.addLocations(outDict['Location'],
            (self['StepSize']*outDict['Dir'],0))
            if not Util.pointWithinBoundingBox(outDict['Location'], \
                Util.getScreen().getSize()):
                outDict['Dir'] *= -1
            ret.append(outDict)
        ret += newResponses
        return (ret, ret)

