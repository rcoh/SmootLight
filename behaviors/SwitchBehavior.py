from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json

class SwitchBehavior(Behavior):
    """
    SwitchBehavior is a behavior that transform into different behaviors base on the input data.
    The behavior expects a JSON formatted argument 'PrefixToBehavior' that maps prefixes to behaviors. The behavior detects the prefix on the data and use the corresponding Behavior to process the data and return the outputs.
    In Config file, include:
      <PrefixToBehavior>JSON format dict with prefix keys and behavior ID values</PrefixToBehavior>
      <DefaultBehavior>Default behavior's ID</DefaultBehavior>
    An example config excerpt:
      <Behavior>
        <Class>behaviors.SwitchBehavior</Class>
          <Args>
            <Id>switch</Id>
            <PrefixToBehavior>{'@':'game1', '#':'game2', '$':'game3'}</PrefixToBehavior>
            <DefaultBehavior>game1</DefaultBehavior>
          </Args>
      </Behavior>
    """
    def behaviorInit(self):
        self.defaultBehavior = compReg.getComponent(self['DefaultBehavior'])
        self.prefixDict = json.loads(self['PrefixToBehavior'])
        self.currBehavior = None
        self.setBehavior(self.defaultBehavior) # init. set currBehavior to be the default one.
        
    def processResponse(self, sInputs, rInputs):
        dataStr = sInputs[-1]['Data']
        if dataStr[0] in self.prefixDict:
            self.setBehavior(compReg.getComponent(self.prefixDict[dataStr[0]]))
            sInputs[-1]['Data'] = sInputs[-1]['Data'][1:] # remove prefix
        return self.currBehavior.immediateProcessInput(sInputs, rInputs)
    
    def setBehavior(self, behavior):
        # can be called by the outside to switch behavior.
        self.currBehavior = behavior
