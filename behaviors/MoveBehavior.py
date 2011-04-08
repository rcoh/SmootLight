from operationscore.Behavior import *
import json
#import util.ComponentRegistry as compReg
#import util.Geo as Geo
#import util.Strings as Strings

class MoveBehavior(Behavior):
    """Moves current location by the x and y components of sensorInput.  Uses recurrences to track
    current input.  @Author: Euguene"""

    def processResponse(self, sensorInputs, recursiveInputs):
        if recursiveInputs:
            currRecLocs = recursiveInputs
        else:
            currRecLocs = [{'Location' : (5, 5), 'Color' : [0, 0, 0]}]

        if sensorInputs:   # if input exists, change location
            ret = []
            for currRecLoc in currRecLocs:
                currDict = dict(currRecLoc)
                for sensorInput in sensorInputs:
                    sInput = json.loads(sensorInput['data'])
                    #print sInput
                    if 'type' in sInput and sInput['type'] == 1:
                        currDict['Shake'] = 0
                        currDict['Location'] = (currDict['Location'][0] - sInput['x'] * self['XStep'], \
                                                currDict['Location'][1] + sInput['y'] * self['YStep'])
                        currDict['Color'] = [sInput['r'], sInput['g'], sInput['b']]
                    elif sInput['type'] == 2:
                        currDict['Shake'] = 1
                        #currDict['Force'] = sInput['force']
                ret.append(currDict)
            #print ret
            return (ret, ret)

        else: # if not, return current recursive location.
            #print currRecLocs
            return (currRecLocs, currRecLocs)
