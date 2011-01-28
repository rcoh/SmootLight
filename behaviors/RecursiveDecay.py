from operationscore.Behavior import *
import pdb
class RecursiveDecay(Behavior):
    """RecursiveDecay is an event to allow recursive hooks to stop recursing after a certain number
    of iterations specified in 
    <InitialResponseCount> -- Int, number of total responses.
    Designed to be used as part of a recursive hook.
    """
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for response in sensorInputs:
            if not 'ResponsesLeft' in response:
                response['ResponsesLeft'] = self['InitialResponseCount']
            else:
                response['ResponsesLeft'] -= 1
            if response['ResponsesLeft'] > 0:
                ret.append(response)
        return (ret, []) #no direct ouput
