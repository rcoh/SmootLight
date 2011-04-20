from operationscore.Behavior import *
import util.TimeOps as clock
import util.ComponentRegistry as compReg
from logger import main_log

class BehaviorSequence(Behavior):
    """BehaviorSequence takes a set of Behaviors as arguements and will
    display them one after another. Takes the following arguments:
    <Args>
        <Id>...</Id>
        <Sequence>
            <Behavior> # Sequence of definition is sequence of display
                <Id>...</Id>
                <Timeout>...</Timeout> # in seconds
                <OnChange>[ None | Pause | Restart ]</OnChange>
                # During the time in which this behavior is not active, what
                # should be going on?
                # Pause: No inputs will be added to it's queue when inactive
                # Restart: Behavior restarts
                # None: Behavior will keep State and will accrue inputs
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
        self.onChange = behavior['OnChange']

    def stopBehavior (self):
        if self.onChange == 'Pause':
            compReg.getComponent(self.behavior).pauseInputs()

    def startBehavior (self):
        if self.onChange == 'Pause':
            compReg.getComponent(self.behavior).resumeInputs()
        elif self.onChange == 'Restart':
            compReg.getCompenent(self.behavior).init()

    def processResponse (self, sensors, state):

        if self.behavior == None:
            return ([], [self.behaviorComplete])
        
        if state == []: # if processResponse has never been run
            for behavior in self['Sequence']:
                if behavior['OnChange'] == 'Pause' \
                        and behavior['Id'] != self.behavior:
                    compReg.getComponent(behavior['Id']).pauseInputs()

        outputs = compReg.getComponent(self.behavior).timeStep()

        loadNext = False
        if len(outputs) > 0 and self.behaviorComplete == outputs[-1]:
            outputs[-1:] = None
            loadNext = True

        if self.endTime <= clock.time() or loadNext == True:

            try:
                self.stopBehavior()
                self.loadNextBehavior()
                self.startBehavior()
            except StopIteration:
                if self['Repeat']:
                    self.behaviorInit()
                    self.startBehavior()
                else:
                    self.behavior = None

        return (outputs, [True])
