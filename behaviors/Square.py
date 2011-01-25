from operationscore.Behavior import *
class Square(Behavior):
        def processResponse(self, sensorInputs, recursiveInputs):
            for sensory in sensorInputs:#TODO: consider replicating the dict
                if 'Location' in sensory:
		        xLoc = sensory['Location'][0]
                        yLoc = sensory['Location'][1]
		        width = self['Width']
                        #sensory['Location'] = 'True'
                        sensory['Location'] =\
                           '{x}<'+str(xLoc+width)+',{x}>'+str(xLoc-width)+\
                           ',{y}<'+str(yLoc+width)+',{y}>'+str(yLoc-width)
            return (sensorInputs, recursiveInputs)
