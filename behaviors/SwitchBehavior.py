from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class SwitchBehavior(Behavior):
    """
    SwitchBehavior is a behavior that transform into different behaviors base on the input data.
    The behavior expects Args in the form of <Prefix>s mapping to <Behavior ID>s. The behavior detects the prefix on the data and use the corresponding Behavior to process the data and return the outputs.
    In Config file, include:
    <Prefix>Behavior's ID<Prefix>
    <DefaultBehavior>Default behavior's ID<DefaultBehavior>
    """
    def behaviorInit(self):
        self.defaultBehavior = compReg.getComponent(self['DefaultBehavior'])
        self.currBehavior = None
        
    def processResponse(self, sInputs, rInputs):
        dataStr = sInputs[-1]['Data']
        if dataStr[0] in self.argDict:
            self.currBehavior = compReg.getComponent(self[dataStr[0]])
            sInputs[-1]['Data'] = sInputs[-1]['Data'][1:] # remove prefix
            return self.currBehavior.processResponse(sInputs, rInputs)
        else:
            return self.defaultBehavior.processsResponse(sInputs, rInputs)
    
