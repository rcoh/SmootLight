from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import logging as main_log
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
            behavior = compReg.getComponent(behaviorId)
            if behaviorId in self.feedback:
                recurrence = self.feedback[behaviorId]
            else:
                recurrence = []
            (response,recurrence) = behavior.immediateProcessInput(response,\
                    recurrence)

            if behaviorId in self.hooks: #process recursive hook if there is one
                hookBehavior = compReg.getComponent(self.hooks[behaviorId])
                #we feed its recurrence in as input to the behavior.  
                (recurrence, hookRecurrence) = \
                hookBehavior.immediateProcessInput(recurrence, \
                        [])
                if hookRecurrence != []:
                    main_log.warn('Hook recurrences are not currently supported.  Implement it\
                        yourself or bug russell')
                self.feedback[behaviorId] = recurrence 
        return response
