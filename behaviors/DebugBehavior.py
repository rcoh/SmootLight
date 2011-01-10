from operationscore.Behavior import * 
from logger import main_log
import pdb
class DebugBehavior(Behavior):
    def processResponse(self, sensorInputs, recursiveInputs):
        if sensorInputs != []:
            main_log.debug('Sensor Inputs: '+ str(sensorInputs))
        return []
