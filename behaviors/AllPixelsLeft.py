from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import pdb
class AllPixelsLeft(Behavior):
    """Behavior which returns all points left of its input.  No Args."""
    def processResponse(self, sensorInputs, recursiveInputs):
        for sensory in sensorInputs:
            xLoc = sensory['Location'][0] 
            sensory['Location'] = '{x}<' + str(xLoc) 
        return (sensorInputs, recursiveInputs)
