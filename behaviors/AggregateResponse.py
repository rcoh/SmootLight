from operationscore.Behavior import *
class AggregateResponse(Behavior):
    def processResponse(self, inputs, state):
        totalLocDict = {}
        outputDict = {}
        inputIndex = len(inputs) 
        for i,r in enumerate(inputs):
            if 'Location' in r:
                locDict = r['Location']
                for key in locDict:
                    if locDict[key] > 0:
                        totalLocDict[key]=locDict[key]
                        if i < inputIndex:
                            inputIndex = i
                        
        if inputs:
            print inputIndex
            outputDict['Color'] = inputs[inputIndex]['Color']
            print outputDict['Color']
            outputDict['Location'] = totalLocDict
            return ([outputDict], []) 
        else:
            return ([],[])

