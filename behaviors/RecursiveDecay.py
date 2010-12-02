from operationscore.Behavior import *
class RecursiveDecay(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for response in recursiveInputs:
            if not 'ResponsesLeft' in response:
                response['ResponsesLeft'] = self['InitialResponseCount']
            else:
                response['ResponsesLeft'] -= 1
            if response['ResponsesLeft'] > 0:
                ret.append(response)
        return (sensorInputs, ret) #no direct ouput
