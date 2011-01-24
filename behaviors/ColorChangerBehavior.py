from operationscore.Behavior import *
import util.ColorOps as color
import pdb
class ColorChangerBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) #don't run into shallow copy issues
            if self['ColorList'] != None:
                newDict['Color'] = color.chooseRandomColor(self['ColorList'])  #TODO: this doesn't work.
            else:
                newDict['Color'] = color.randomColor() 
            ret.append(newDict)
        return (ret, [])
