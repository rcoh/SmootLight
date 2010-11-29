from operationscore.Behavior import *
import Util
import pdb
class BehaviorChain(Behavior):
    def behaviorInit(self):
        self.feedback = {} #dictionary to allow feedback of recursives
    def processResponse(self, sensorInputs, recursiveInputs):
        response = sensorInputs
        for behaviorId in self['ChainedBehaviors']:
            behavior = Util.getComponentById(behaviorId)
            if behaviorId in self.feedback:
                recurrence = self.feedback[behaviorId]
            else:
                recurrence = []
            (response,recurrence) = behavior.immediateProcessInput(response,\
                    recurrence)
            self.feedback[behaviorId] = recurrence
        return response
