from operationscore.Behavior import *
class AllPixels(Behavior):
        def processResponse(self, sensorInputs, recursiveInputs):
            for sensory in sensorInputs:#TODO: consider replicating the dict
                sensory['Location'] = 'True'
            return (sensorInputs, recursiveInputs)
