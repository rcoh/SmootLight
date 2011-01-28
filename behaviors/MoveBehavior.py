from operationscore.Behavior import *
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
            currRecLocs = [{'Location' : (5, 5), 'Color' : [255, 255, 255]}]

        #print sensorInputs
        if sensorInputs:   # if input exists, change location
            ret = []
            for currRecLoc in currRecLocs:
                currDict = dict(currRecLoc)
                for sensorInput in sensorInputs:
                    if 'type' in sensorInput and int(sensorInput['type']) == 1:
                        #currDict['Shake'] = 0
                        currDict['Location'] = (currDict['Location'][0] - int(sensorInput['x']) * self['XStep'], \
                                                currDict['Location'][1] + int(sensorInput['y']) * self['YStep'])
                        currDict['Color'] = [int(sensorInput['r']), int(sensorInput['g']), int(sensorInput['b'])]
                    elif int(sensorInput['type']) == 2:
                        #print sensorInput
                        currDict['Shake'] = 1
                        #currDict['Force'] = sensorInput['force']
                ret.append(currDict)
            return (ret, ret)

        else: # if not, return current recursive location.
            #print currRecLocs
            return (currRecLocs, currRecLocs)
