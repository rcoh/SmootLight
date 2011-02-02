from operationscore.Behavior import *
import util.TimeOps as timeops
class Timeout(Behavior):
    """Timeout is a behavior designed to be used in recursive hooks to stop responses after a certain
    amount of time.  It is the Time-version of RecursiveDecay.  Specify:
    <TimeOut> -- the time in ms that the response will run.
    """
    
    def processResponse(self,sensorInputs, recur):
        ret = []
        for data in sensorInputs:
            if not 'StartTime' in data:
                data['StartTime'] = timeops.time()
            if timeops.time()-data['StartTime'] < self['Timeout']:
                ret.append(data)
        return (ret,[])
