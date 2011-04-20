from operationscore.Behavior import * 
from logger import main_log
import pdb
class DebugBehavior(Behavior):
    """DebugBehavior simply writes all of its inputs to the logs, currently at the ERROR level for
    easy visibility.  Will be changed to DEBUG or INFO in the future
    
    An optional <Output> tag can be added to direct the sensor information.
    Currently, the options are print, error, debug, and info. Default is error
    An optional <PassThrough> tag can be added to prevent debug behavior from
    passing inputs on. Default is False
    An optional <Quiet> tag can be added to prevent debug behavior from dumping
    unless sensorInputs is nonempty. Default is True
    """

    def processResponse(self, sensorInputs, recursiveInputs):
        debug_string = "DebugBehavior<" + self['Id'] + ">\n"

        if sensorInputs == [] and 'Quiet' in self.argDict and self['Quiet']:
            return ([], [])

        if sensorInputs == []:
            debug_string += "\tNO INPUTS"
        else:
            for sensorInput in sensorInputs:
                debug_string += '\t' + str(sensorInput) + '\n'

        if 'Output' in self.argDict:
            if self['Output'] == 'print':
                print debug_string
            elif self['Output'] == 'error':
                main_log.error(debug_string)
            elif self['Output'] == 'debug':
                main_log.debug(debug_string)
            elif self['Output'] == 'info':
                main_log.info(debug_string)
        else:
            if sensorInputs != []:
                main_log.error('Sensor Inputs: ' + str(sensorInputs))

        if 'PassThrough' in self.argDict:
            if self['PassThrough']:
                return (sensorInputs, [])
            else:
                return ([], [])

        return ([], [])
