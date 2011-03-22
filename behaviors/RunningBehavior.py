from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Geo as Geo
import pdb
class RunningBehavior(Behavior):
    """RunningBehavior is a straightforward behavior that makes a Location run back and forth across
    a screen.  Specify:
    <StepSize> -- the length of movment in units when the response moves.
    """

    def processResponse(self, sensorInputs, recursiveInputs):
        newResponses = sensorInputs 
        ret = []
        ret += newResponses
        for recurInput in recursiveInputs:
            outDict = dict(recurInput)
            if not 'Dir' in outDict:
                outDict['Dir'] = 1 #to the right
            if not 'StepSize' in outDict:
                outDict['StepSize'] = self['StepSize']
            outDict['Location']= Geo.addLocations(outDict['Location'],
            (outDict['StepSize']*outDict['Dir'],0))
            
            if not Geo.pointWithinBoundingBox(outDict['Location'], \
                compReg.getComponent('Screen').size):
                    outDict['Dir'] *= -1
            ret.append(outDict)
        ret += newResponses
        return (ret, ret)

