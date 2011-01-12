import pdb
from operationscore.Behavior import *
import util.ComponentRegistry as compReg
#ResponseMover is a scaffold for behaviors that spawn 'walkers' which act autonomously on input.
#Add a recursive hook to control the movement.  
class ResponseMover(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        newResponses = sensorInputs 
        ret = []
        for recurInput in recursiveInputs:
            outDict = dict(recurInput)
            ret.append(outDict)
        ret += newResponses
        return (ret, ret)
    
