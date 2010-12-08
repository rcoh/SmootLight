from operationscore.Behavior import *
import Util
import pdb
class ColorChangerBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) #don't run into shallow copy issues
            if self['ColorList'] != None:
                newDict['Color'] = Util.chooseRandomColor(self['ColorList'])  #TODO: this doesn't work.
            else:
                newDict['Color'] = Util.randomColor() 
#newDict['Color'] = (255,0,0)
            ret.append(newDict)
        return (ret, recursiveInputs)
