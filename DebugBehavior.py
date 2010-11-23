from Behavior import Behavior
import Util
import pdb
class DebugBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        if sensorInputs != []:
            print 'Sensor Inputs: ', sensorInputs
        return []
