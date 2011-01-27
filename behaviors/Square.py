from operationscore.Behavior import *
class Square(Behavior):
    """Square is a simple behavior that makes a square with side lengths Width*2 around locations in
    the sensor input.  Specify:
    <Width> -- the sidelength/2
    """

    def processResponse(self, sensorInputs, recursiveInputs):
        for sensory in sensorInputs:#TODO: consider replicating the dict
            xLoc = sensory['Location'][0]
            yLoc = sensory['Location'][1]
            width = self['Width']
            #sensory['Location'] = 'True'
            sensory['Location'] =\
                '{x}<'+str(xLoc+width)+',{x}>'+str(xLoc-width)+\
                ',{y}<'+str(yLoc+width)+',{y}>'+str(yLoc-width)
        return (sensorInputs, recursiveInputs)
