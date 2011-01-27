from operationscore.Behavior import *
class AllPixels(Behavior):
    """Turns on all Pixels in the installation.  Must use SimpleMapper, or other Mapper supporting
    conditional pixel locations."""
    
    def processResponse(self, sensorInputs, recursiveInputs):
        for sensory in sensorInputs:#TODO: consider replicating the dict
            sensory['Location'] = 'True'
        return (sensorInputs, recursiveInputs)
