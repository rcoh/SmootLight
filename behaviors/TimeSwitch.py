from operationscore.Behavior import *
import util.TimeOps as clock
import util.ComponentRegistry as compReg
from logger import main_log
class TimeSwitch(Behavior):
    """TimeSwitch is a behavior that alternates between different behaviors for a set amount of time
    (specify time in seconds.  Specify in a python-style dict:
        <Behaviors>{'behaviorId1':60, 'behaviorId2':120}</Behaviors>
    Would alternate between the 2 behaviors, spending 1 minute on b1 and 2 minutes on b2.
    """
    def behaviorInit(self):
        self.keyIndex = 0
        self.currentBehaviorId = self['Behaviors'].keys()[self.keyIndex]
        self.behaviorStart = clock.time()

    def processResponse(self, sensors, recurs):
        if self.behaviorStart + self['Behaviors'][self.currentBehaviorId]*1000 <= clock.time():
            self.keyIndex += 1
            self.keyIndex = self.keyIndex % len(self['Behaviors'])
            self.currentBehaviorId = self['Behaviors'].keys()[self.keyIndex]
            self.behaviorStart = clock.time()
            main_log.info('Switching behaviors')
        return compReg.getComponent(self.currentBehaviorId).processResponse(sensors, recurs)
        
