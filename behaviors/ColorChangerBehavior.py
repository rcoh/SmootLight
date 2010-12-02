from operationscore.Behavior import *
import Util
import pdb
class ColorChangerBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) #don't run into shallow copy issues
            if self['ColorList'] != None:
                newDict['Color'] = Util.randomColor(self['ColorList']) 
            else:
                newDict['Color'] = Util.chooseRandomColor() 
            ret.append(newDict)
        return ret
