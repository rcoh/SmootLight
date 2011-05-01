import pdb
from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import random
class TDMAMover(Behavior):
    """ResponseMover is a scaffold for behaviors that spawn 'walkers' which act autonomously on input.
    To control the movment, use the behavior as part of a BehaviorChain and add a recursive hook which
    modulates the location."""

    def processResponse(self, sensorInputs, recursiveInputs):
        numObjs = len(recursiveInputs)
        recurs = recursiveInputs+self.addUID(sensorInputs), numObjs
        index = random.randint(0, numObjs)
        output = []
        for r in recursiveInputs:
            if r['TDMAId']-r % 100 == 0:
                output.append(r)
        return (output, recurs)
    def addUIDAndTMDA(self, inputs, numObjs):
        for i in inputs:
            i['UniqueResponseIdentifier'] = compReg.getNewId()
            i['TDMAId'] = numObjs
            numObjs += 1
        return inputs
    
