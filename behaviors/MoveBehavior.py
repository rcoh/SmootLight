from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Geo as Geo
import util.Strings as Strings

class MoveBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        if recursiveInputs:
            currRecLocs = recursiveInputs
        else:
            currRecLocs = [{'Location' : (5, 5), 'Color' : [255, 255, 255]}]

        if sensorInputs:   # if input exists, change location
            ret = []
            for currRecLoc in currRecLocs:
                currDict = dict(currRecLoc)
                for sensorInput in sensorInputs:
                    currDict['Location'] = (currDict['Location'][0] - sensorInput['x'] * self['XStep'], \
                                            currDict['Location'][1] + sensorInput['y'] * self['YStep'])
                    currDict['Color'] = [sensorInput['r'], sensorInput['g'], sensorInput['b']]
                ret.append(currDict)
            #print ret
            return (ret, ret)

        else: # if not, return current recursive location.
            #print currRecLocs
            return (currRecLocs, currRecLocs)
