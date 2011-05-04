from operationscore.Behavior import *
import util.ColorOps as color
import pdb
import colorsys
import random
class RandomSetColorBehavior(Behavior):
    """Sets a random color that is bright."""
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) 
            newDict['Color'] = color.randomDimColor(self.argDict['Dimness']) 
            ret.append(newDict)
        return (ret, [])
