
from operationscore.Behavior import *
import math
import util.TimeOps as timeOps
#Required Args:
#Period (ms), MaxHeight, Width
class Sink(Behavior):
    """RiseFall is a behavior that creates a rising and falling column of light.  Specify:
    <MaxHeight> -- the maximum height that it rises to.
    <Width> -- the width of the column OR <Left> and <Right>
    <Period> -- the period of oscillation in ms

    Designed to be used as part of a recursive hook.
    """

    def processResponse(self, sensorInputs, recurInputs):
        ret = []
        for data in sensorInputs:
            #first time with behavior:
            data = dict(data)
            if not 'StartTime' in data:
                data['StartTime'] = timeOps.time()
                data['Period'] = self['Period']
                data['MaxHeight'] = self['MaxHeight']  #Consider just using +=
                if not 'Bottom' in data:
                    data['Bottom'] = data['Location'][1]
                if 'Width' in self: #TODO: improve
                    data['Width'] = self['Width']
                    data['Left'] = data['Location'][0]-data['Width']/2.
                    data['Right'] = data['Location'][0]+data['Width']/2.
            currentTime = timeOps.time()
            deltaTime = currentTime-data['StartTime']
            data['Height'] = data['MaxHeight']*math.cos(deltaTime/data['Period']*(math.pi*2))

            data['Location'] = "{x}>"+str(data['Left']) + ", " +\
            "{x}<"+str(data['Right'])+", {y}<" + str(data['Bottom']) + ",\
            {y}>"+str(data['Bottom']-data['Height'])

            ret.append(data)
        return (ret, [])


