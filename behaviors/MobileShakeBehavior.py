from operationscore.Behavior import *
import util.Strings as Strings

class MobileShakeBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        #print sensorInputs
        ret = []
        for sInput in sensorInputs:
            outDict = dict(sInput)
            if 'type' in sInput and sInput['type'] == 2:
                outDict['Location'] = '{x}>' + str(0) + ',{y}>' + str(0)
                outDict['Color'] = [sInput['r'], sInput['g'], sInput['b']]
            else: # dumb invisible pixel
                outDict['Location'] = (-1, -1)
                outDict['Color'] = [0, 0, 0]
            ret.append(outDict)
        return (ret, recursiveInputs)
