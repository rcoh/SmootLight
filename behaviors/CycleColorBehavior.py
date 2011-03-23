from operationscore.Behavior import *
import util.ColorOps as color
import pdb
class CycleColorBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
	index = 0
        for sensory in sensorInputs:
            newDict = dict(sensory) 
            newDict['Color'] = color.cycleColor(newDict['Location'][0], self['Increments'])
            ret.append(newDict)
	    index += 1
        return (ret, [])
