from operationscore.Behavior import *
import util.TimeOps as clock
import util.ComponentRegistry as compReg
from logger import main_log

class BehaviorSequence(Behavior):
    """BehaviorSequence takes a set of Behaviors as arguements and will
    display them in one after another. Takes the following arguments:
    <Args>
        <Id>...</Id>
        <Inputs> # List of all inputs to be routed to sequenced behaviors
            <Id>...</Id>
            ...
        </Inputs>
        <Sequence>
            <Behavior> # Sequence of definition is sequence of display
                <Id>...</Id>
                <Timeout>...</Timeout> # in seconds
                <Inputs> # List of inputs that should route to this behavior
                    <Id>...</Id>
                    ...
                </Inputs>
            </Behavior>
            ...
        </Sequence>
        <Repeat>[True | False]</Repeat> 
        # boolean: if true, then when BehaviorSequence finishes the last
        # sequenced behavior it will return a single state dictionary:
        # {BehaviorComplete: True} and will drop any further inputs/outputs.
        # if false, then BehaviorSequence will simply loop back its first
        # sequenced behavior and start again
    </Args>
    Behaviors will change when either the last output of the currently
    executing behavior is {BehaviorComplete: True}, or the behavior runs to 
    the specified timeout."""

    behaviorComplete = {'BehaviorComplete': True}

    def behaviorInit (self):
        print "behaviorInit"
        self.iterator = self['Sequence'].__iter__()
        self.loadNextBehavior()

    def loadNextBehavior (self):
        print "loadNextBehavior"
        behavior = self.iterator.next()
        print "   ", behavior
        self.behavior = behavior['Id']
        self.endTime = clock.time() + behavior['Timeout'] * 1000

    def processResponse (self, sensors, state):

        if self.behavior == None:
            return ([], [self.behaviorComplete])
        
        outputs = compReg.getComponent(self.behavior).timeStep()

        loadNext = False
        if len(outputs) > 0 and self.behaviorComplete == outputs[-1]:
            outputs[-1:] = None
            loadNext = True

        if self.endTime <= clock.time() or loadNext == True:

            try:
                self.loadNextBehavior()
                #compReg.getComponent(self.behavior).clearInputs()
            except StopIteration:
                if self['Repeat']:
                    self.behaviorInit()
                    #compReg.getComponent(self.behavior).clearInputs()
                else:
                    self.behavior = None

        return (outputs, state)
