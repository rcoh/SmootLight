import pdb
from operationscore.Behavior import *
import util.ComponentRegistry as compReg
class MonitoredMover(Behavior):
    """
    MonitoredMover is a scaffold for behaviors that spawn 'walkers' which act autonomously on input.
    To control the movment, use the behavior as part of a BehaviorChain and add a recursive hook which
    modulates the location.
    - 1 added feature is ['IntervalCount'], which controls the countdown #, only after which would inputs
      be let through
    """
    def behaviorInit(self):
        self.currCount = self['IntervalCount']

    def processResponse(self, sensorInputs, recursiveInputs):
        #print self.currCount
        if self.currCount <= 0:
            a = (recursiveInputs, recursiveInputs+self.addUID(sensorInputs))
            self.currCount = self['IntervalCount']
        else:
            a = ([], recursiveInputs)
            self.currCount -= 1
            
        return a
    
    def addUID(self, inputs):
        for i in inputs:
            i['UniqueResponseIdentifier'] = compReg.getNewId()
        return inputs
    
