from operationscore.Behavior import *
class AllPixels(Behavior):
    """Turns on all Pixels in the installation.  Must use FunctionMapper, or other Mapper supporting
    conditional pixel locations."""

    location = eval('lambda x,y,z: True')
    
    def processResponse(self, sensorInputs, recursiveInputs):
        for sensory in sensorInputs:#TODO: consider replicating the dict
            sensory['Location'] = self.location
        return (sensorInputs, recursiveInputs)
