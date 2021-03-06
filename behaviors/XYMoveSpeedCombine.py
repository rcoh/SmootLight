from operationscore.Behavior import *
import util.BehaviorQuerySystem as bqs
import util.Geo as Geo
class XYMoveSpeedCombine(Behavior):
    """XYMoveSpeedCombine is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XStep and YStep.  As XStep and YStep are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XStep> -- the starting XStep
    <YStep> -- the starting YStep
    """

    def processResponse(self, sensor, recurs):
        ret = []
        for sensory in sensor:
            opsensory = dict(sensory)
            self.insertStepIfMissing(opsensory) 
            #TODO: update 19 to be a configurable variable
            results = bqs.query([
                bqs.getBehaviorIdLambda(self['Id']),\
                bqs.getDifferentUIDLambda(opsensory['UniqueResponseIdentifier']),\
                bqs.getDistLambda(opsensory['Location'], 19)
            ])
            if results:
                for result in results:
                    new = opsensory['XStep'] + result['XStep']
                    if new>=0:
                        opsensory['XStep'] = min(20, new)
                    if new<0:
                        opsensory['XStep'] = max(-20, new)
            opsensory['Location'] = Geo.addLocations((opsensory['XStep'], opsensory['YStep']), opsensory['Location']) 
            ret.append(opsensory)
        return (ret, []) 

    def insertStepIfMissing(self, data):
        if not 'XStep' in data:
            data['XStep'] = self['XStep']
        if not 'YStep' in data:
            data['YStep'] = self['YStep']
