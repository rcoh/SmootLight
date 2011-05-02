from operationscore.Behavior import *
import util.Geo as Geo
import util.Strings as Strings
import pdb
class HorizontalClone(Behavior):
    """
    HorizontalClone takes an input and clones it around its location for specified times horizontally.
    - ['StepSize']: cloned unit distance away from the input
    - ['Times']: # of times the input gets cloned.
    """
    def processResponse(self, sensors, recursives):
        ret = []
        for sensory in sensors:
            for i in range(1, self['Times']/2):
                clonedLocLeft = (sensory[Strings.LOCATION][0] - i*self['StepSize'], sensory[Strings.LOCATION][1])
                if clonedLocLeft not in sensory[Strings.LOCATION]:
                    ret.append({Strings.LOCATION: clonedLocLeft})
                clonedLocRight = (sensory[Strings.LOCATION][0] + i*self['StepSize'], sensory[Strings.LOCATION][1])
                if clonedLocRight not in sensory[Strings.LOCATION]:
                    ret.append({Strings.LOCATION: clonedLocRight})
        return (ret, [])
