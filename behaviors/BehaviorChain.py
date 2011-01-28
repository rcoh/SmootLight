from operationscore.Behavior import *
import util.ComponentRegistry as compReg
from logger import main_log
import pdb
class BehaviorChain(Behavior):
    """BehaviorChain is a class which chains together multiple behavior.  BehaviorChain is in itself a
    behavior, and behaves and can be used accordingly.  BehaviorChain also supports recursive hooks to
    be set on its constituent behaviors.  ChainedBehaviors should be specified in <Args> as follows:

    <ChainedBehaviors>
        <Id>behavior1Id</Id>
        <Id>behavior2Id</Id>
    </ChainedBehaviors>

    Behaviors may also be appended programmatically via the appendBehavior method.

    Recursive hooks should be specified with Python dict syntax as follows:

    <RecursiveHooks>{'behavior1Id':'hookid'}</RecursiveHooks>

    Behavior Chain manages all recurrences that its constituents propogate.  At this point, it does not
    support recurrences in its hooks."""

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
                    main_log.warn('Hook recurrences are not currently supported.') 
            self.feedback[behaviorId] = recurrence 
        return (response, [])
    
    def appendBehavior(behavior):
        bid = compReg.registerComponent(behavior) #register behavior (will make
        #a new id if there isn't one)
        self['ChainedBehaviors'].append(bid)

