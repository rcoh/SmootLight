from operationscore.Behavior import *
import Util
import pdb
class BehaviorChain(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        response = sensorInputs
        for behaviorId in self['ChainedBehaviors']:
            behavior = Util.getComponentById(behaviorId)
            response = behavior.immediateProcessInput(response)
        return response
