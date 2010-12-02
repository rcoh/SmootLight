from operationscore.Behavior import *
import Util
import pdb
class BehaviorChain(Behavior):
    def behaviorInit(self):
        self.feedback = {} #dictionary to allow feedback of recursives
        self.hooks = self['RecursiveHooks']
        if self.hooks == None:
            self.hooks = {}
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

            if behaviorId in self.hooks: #process recursive hook if there is one
                hookBehavior = Util.getComponentById(self.hooks[behaviorId])
                (response, recurrence) = \
                hookBehavior.immediateProcessInput(response,
                        recurrence)
            self.feedback[behaviorId] = recurrence
        return response
