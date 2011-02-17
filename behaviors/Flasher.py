
from operationscore.Behavior import *
import util.ColorOps as colorops
import pdb
class Flasher(Behavior):
    """Implements a pulsing/flashing behavior.
     Jim Salem 

     Args:
       Factor - The speed of flashing. Must be b/w 0 and 1.  Default is .95
    """
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for response in sensorInputs:
            # Get the multiplier
            if self['Factor'] != None:
                factor = self['Factor']
            else:
                factor = 0.95
            # Initialize the first time
            if not 'FireflyStartColor' in response:
                response['FireflyValue'] = 1.0
                response['FireflyDir'] = 1
                response['FireflyStartColor'] = response['Color'];
            else:
                # Update the current value
                if response['FireflyDir'] == 1:
                    response['FireflyValue'] = response['FireflyValue'] * factor
                    if response['FireflyValue'] <= 0.01:
                        response['FireflyValue'] = 0.01
                        response['FireflyDir'] = 0
                else:
                    response['FireflyValue'] = response['FireflyValue'] / factor
                    if response['FireflyValue'] >= 1.0:
                        response['FireflyValue'] = 1.0
                        response['FireflyDir'] = 1

            # Compute the color
            response['Color'] = colorops.multiplyColor(response['FireflyStartColor'], response['FireflyValue'])
            ret.append(response)
        return (ret, []) #no direct ouput
