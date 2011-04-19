from operationscore.Behavior import *
import util.BehaviorQuerySystem as bqs
import util.Geo as Geo
class XYMoveBounceDirOne(Behavior):
    """XYMoveBounceDirOne is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XStep and YStep.  As XStep and YStep are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XStep> -- the starting XStep
    <YStep> -- the starting YStep
    """

    def processResponse(self, sensor, recurs):
        ret = []
        for sensory in sensor:
            opsensory = dict(sensory)
            isNew = self.insertStepIfMissing(opsensory) 
            #TODO: update 19 to be a configurable variable
            if opsensory['isNew'] <= 0:
                results = bqs.query([
                    bqs.getBehaviorIdLambda(self['Id']),\
                    bqs.getDifferentUIDLambda(opsensory['UniqueResponseIdentifier']),\
                    bqs.getDistLambda(opsensory['Location'], 19)
                ])
                if results:
                    opsensory['XStep'] = -opsensory['XStep']
                    opsensory['Location'] = Geo.addLocations((opsensory['XStep'], opsensory['YStep']), opsensory['Location']) 
            else:
                opsensory['isNew'] -= 1
            if isNew:
                if opsensory['Direction'] < 0:
                    opsensory['XStep'] = -opsensory['XStep']
                if opsensory['Direction'] != 0:
                    opsensory['Location'] = Geo.addLocations((2*opsensory['XStep'], opsensory['YStep']), opsensory['Location']) 
                    ret.append(opsensory)
            else:
                opsensory['Location'] = Geo.addLocations((opsensory['XStep'], opsensory['YStep']), opsensory['Location']) 
                ret.append(opsensory)
        return (ret, []) 

    def insertStepIfMissing(self, data):
        isNew = False
        if not 'XStep' in data:
            data['XStep'] = self['XStep']
            isNew = True
            data['isNew'] = self['NoBounceTime']
        if not 'YStep' in data:
            data['YStep'] = self['YStep']
            isNew = True
            data['isNew'] = self['NoBounceTime']
        return isNew

