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
                <Id>...</Id> # Id of root animation behavior
                <Timeout>...</Timeout> # in seconds, run time for behavior
                <OnChange>[ None | Pause | Restart ]</OnChange>
                # During the time in which this behavior is not active, what
                # should be going on?
                # Pause: No inputs will be added to it's queue when inactive
                # Restart: Behavior restarts when reactivated
                # None: Behavior will keep State and will accrue inputs
                <FadeInId>...</FadeInId> # optional behavior to modulate fadein
                <FadeInTime>...</FadeInTime> # fade in time in seconds
                <FadeOutId>...</FadeOutId> # optional behavior
                <FadeOutTime>...</FadeOutTime> # in seconds
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
    the specified timeout.
    Note that BehaviorSequence itself does not accept inputs; instead, inputs
    should be specified in the root animation behavior, i.e. if BehaviorSeq.
    does not exist."""

    behaviorComplete = {'BehaviorComplete': True}

    def behaviorInit (self):
        print self['Id'], "behaviorInit"
        self.iterator = self['Sequence'].__iter__()
        self.loadNextBehavior()
        self.transition = None

    def loadNextBehavior (self):
        print self['Id'], "loadNextBehavior"
        behavior = self.iterator.next()
        print self['Id'], "   ", behavior
        self.behavior = behavior['Id']
        self.onChange = behavior['OnChange']
        if 'FadeInId' in behavior:
            self.transin = behavior['FadeInId']
            self.endTime = clock.time() + behavior['FadeInTime'] * 1000
            self.timeout = behavior['Timeout']
        else:
            self.transin = None
            self.endTime = clock.time() + behavior['Timeout'] * 1000
        if 'FadeOutId' in behavior:
            self.transout = behavior['FadeOutId']
            self.fadetime = behavior['FadeOutTime']
        else:
            self.transout = None
            self.fadetime = 0

    def stopBehavior (self):
        print self['Id'], "stop Behavior", self.behavior
        if self.transout:
            self.transoutState = \
                compReg.getComponent(self.transout).behaviorInit()
        self.transition = self.behavior
        self.transitionout = self.transout
        self.transTime = clock.time() + self.fadetime * 1000
        self.transout = None
        self.transOnChange = self.onChange
        self.onChange = None

    def startBehavior (self):
        print self['Id'], "startBehavior", self.behavior
        if self.transin:
            self.transinState =  \
                compReg.getComponent(self.transin).behaviorInit()
        if self.onChange == 'Pause':
            compReg.getComponent(self.behavior).resumeInputs()
        elif self.onChange == 'Restart':
            compReg.getCompenent(self.behavior).init()

    def transitionIn (self): # switch out of fade in
        print self['Id'], "transitionIn ", self.transin
        self.transin = None
        self.transinState = []
        self.endTime = clock.time() + self.timeout * 1000

    def transitionOut (self): #switch out of fade out
        print self['Id'], "transitionOut", self.transition
        if self.transOnChange == 'Pause':
            compReg.getComponent(self.transition).pauseInputs()
        self.transition = None
        self.transitionout = None
        self.transoutState = []

    def processResponse (self, sensors, state):

        curTime = clock.time()

        if state == []: # if processResponse has never been run
            for behavior in self['Sequence']:
                if behavior['OnChange'] == 'Pause':
                    compReg.getComponent(behavior['Id']).pauseInputs()
            self.startBehavior()

        if self.behavior:
            outputs = compReg.getComponent(self.behavior).timeStep()
            loadNext = False
            if len(outputs) > 0 and self.behaviorComplete == outputs[-1]:
                outputs[-1:] = None
                loadNext = True

            if self.transin:
                transin = compReg.getComponent(
                    self.transin).immediateProcessInput(
                                                outputs, self.transinState)
                outputs = transin[0]
                self.transinState = transin[1]

        if self.transition and self.transitionout:
            transoutput = compReg.getComponent(self.transition).timeStep()
            transout = compReg.getComponent(
                self.transitionout).immediateProcessInput(
                                            transoutput, self.transoutState)
            compReg.getComponent(self.transition).setLastOutput(transout[0])
            outputs.extend(transout[0])
            self.transoutState = transout[1]

        if self.endTime <= curTime or loadNext == True:

            try:
                if self.transin and not loadNext:
                    self.transitionIn()
                else:
                    self.stopBehavior()
                    self.loadNextBehavior()
                    self.startBehavior()
            except StopIteration:
                if self['Repeat']:
                    self.behaviorInit()
                    self.startBehavior()
                else:
                    self.behavior = None

        if self.transition and self.transTime <= curTime:
            self.transitionOut()

        return (outputs, [True])

    def pauseInputs(self):
        print self['Id'], "paused input"
        self.inputPause = True
        for behavior in self['Sequence']:
            if behavior['OnChange'] == 'Pause':
                compReg.getComponent(behavior['Id']).pauseInputs()
    def resumeInputs(self):
        print self['Id'], "resumed input"
        self.inputPause = False
        for behavior in self['Sequence']:
            if behavior['OnChange'] == 'Pause':
                compReg.getComponent(behavior['Id']).resumeInputs()
