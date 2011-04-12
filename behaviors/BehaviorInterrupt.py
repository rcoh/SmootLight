from operationscore.Behavior import *
import util.TimeOps as clock
import util.ComponentRegistry as compReg
from logger import main_log

class BehaviorInterrupt(Behavior):
    """This Behavior takes two Behaviors, denoted Main and Interrupt.
    It will run as if it were Main until it detects an input queued for
    Interrupt, at which point it will switch to running as Interrupt until
    a specified number of milliseconds after the last detected input to
    Interrupt, when it will resume running as Main.

    BehaviorInterrupt takes the following arguments:
    <Args>
        <Id>...</Id>
        <MainId>...</MainId>
        <OnChange>[ None | Pause | Restart]</OnChange>
        <InterruptId>...</InterruptId>
        <Timeout>...</Timeout> # in seconds
    </Args>

    OnChange tags say during the time in which this behavior is not active, 
    what should be going on:
        Pause: No inputs will be added to it's queue when inactive
        Restart: Behavior restarts
        None: Behavior will keep State and will accrue inputs"""

    def initialized(self):
        pass

    def initializing(self):
        print "BehaviorInterrupt initializing"
        self.main = compReg.getComponent(self['MainId'])
        self.interrupt = compReg.getComponent(self['InterruptId'])
        self.last_interrupt = 0
        self.initialize = self.initialized

    initialize = initializing

    def stoppingMain (self):
        print "stoppingMain"
        if self['OnChange'] == 'Pause':
            self.main.pauseInputs()
        self.stopMain = self.stoppedMain
        self.startMain = self.startingMain
    def stoppedMain (self):
        pass

    stopMain = stoppingMain

    def startingMain (self):
        print "startingMain"
        if self['OnChange'] == 'Pause':
            self.main.resumeInputs()
        elif self['OnChange'] == 'Restart':
            self.main.init()
        self.startMain = self.startedMain
        self.stopMain = self.stoppingMain
    def startedMain (self):
        pass

    startMain = startingMain

    def processResponse (self, inputs, state):

        self.initialize()
        
        if self.interrupt.sensorResponseQueue != []:
            self.stopMain()
            self.last_interrupt = clock.time()

        if self.last_interrupt + self['Timeout'] * 1000 >= clock.time():
            outputs = self.interrupt.timeStep()
        else:
            self.startMain()
            outputs = self.main.timeStep()

        return (outputs, [True])
