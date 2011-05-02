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

        if self['NoBounceTime'] != None:
            noBounceTime = self['NoBounceTime']
        else:
            noBounceTime = 1000
        if self['BQSDistance'] != None:
            BQSDistance = self['BQSDistance']
        else:
            BQSDistance = 19


        for sensory in sensor:
            opsensory = dict(sensory)

            isNew = self.insertStepIfMissing(opsensory) 
            if not 'NoBounceTime' in opsensory:
                opsensory['NoBounceTime'] = noBounceTime 

            if opsensory['NoBounceTime'] <= 0:
                results = bqs.query([
                    bqs.getBehaviorIdLambda(self['Id']),\
                    bqs.getDifferentUIDLambda(opsensory['UniqueResponseIdentifier']),\
                    bqs.getDistLambda(opsensory['Location'], BQSDistance)
                ])
                if results:
                    opsensory['XStep'] = -opsensory['XStep']
                    opsensory['Location'] = Geo.addLocations((opsensory['XStep'], opsensory['YStep']), opsensory['Location']) 
            else:
                opsensory['NoBounceTime'] -= 1
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
        if not 'YStep' in data:
            data['YStep'] = self['YStep']
            isNew = True
        return isNew

