from operationscore.Behavior import *
class AggregateResponse(Behavior):
    def processResponse(self, inputs, state):
        totalLocDict = {}
        outputDict = {}
        for r in inputs:
            if 'Location' in r:
                locDict = r['Location']
                for key in locDict:
                    totalLocDict[key]=locDict[key]
        if inputs:
            outputDict['Color'] = inputs[-1]['Color']
            outputDict['Location'] = totalLocDict
            return ([outputDict], []) 
        else:
            return ([],[])

