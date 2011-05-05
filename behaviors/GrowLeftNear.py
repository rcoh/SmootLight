from operationscore.Behavior import *
import util.BehaviorQuerySystem as bqs
import util.Geo as Geo
class GrowLeftNear(Behavior):
    """GrowLeftNear is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XStep.  As XStep are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XStep> -- the starting XStep
    """

    def processResponse(self, sensor, recurs):
        ret = []
        for sensory in sensor:
            opsensory = dict(sensory)
            #TODO: update 19 to be a configurable variable
            self.insertVelIfMissing(opsensory)
            results = bqs.query([
                bqs.getBehaviorIdLambda('accelerate'),\
                bqs.getDirectionLambda('+'),\
                bqs.getDistLambda(opsensory['Location'], 38)
            ])
            if results:
                opsensory['XVel'] = opsensory['XVel'] + 10 
            opsensory['XVel'] = min(max(-1, opsensory['XVel'] - 1), 10)
            opsensory['Location'] = Geo.addLocations((-opsensory['XVel'], 0), opsensory['Location'])
            if opsensory['Location'][0] >= 800: #TODO: Make this dynamic
                opsensory['Location'] = tuple([799, 25])
            ret.append(opsensory)
        return (ret, []) 
    def insertVelIfMissing(self, data):
        if not 'XVel' in data:
            data['XVel'] = -1

