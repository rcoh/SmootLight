from operationscore.Behavior import * 
from logger import main_log
import pdb
class DebugBehavior(Behavior):
    """DebugBehavior simply writes all of its inputs to the logs, currently at the ERROR level for
    easy visibility.  Will be changed to DEBUG or INFO in the future"""

    def processResponse(self, sensorInputs, recursiveInputs):
        if sensorInputs != []:
            main_log.error('Sensor Inputs: ' + str(sensorInputs))
        return ([], [])
