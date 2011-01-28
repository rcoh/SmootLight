from operationscore.Behavior import *
import util.ColorOps as color
import pdb
import colorsys
import random
class RandomSetBrightColorBehavior(Behavior):
    """Sets a random color that is bright."""
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) 
            newDict['Color'] = color.randomBrightColor() 
            ret.append(newDict)
        return (ret, [])
