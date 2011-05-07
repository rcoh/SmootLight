from operationscore.Behavior import *
import util.BehaviorQuerySystem as bqs
import util.Geo as Geo
class XYMoveBounceDirOne(Behavior):
    """XYMoveBounceDirOne is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XVel and YVel.  As XVel and YVel are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XVel> -- the starting XVel
    <YVel> -- the starting YVel
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

            isNew = self.insertVelIfMissing(opsensory) 
            if not 'NoBounceTime' in opsensory:
                opsensory['NoBounceTime'] = noBounceTime 

            if opsensory['NoBounceTime'] <= 0:
                results = bqs.query([
                    bqs.getBehaviorIdLambda(self['Id']),\
                    bqs.getDifferentUIDLambda(opsensory['UniqueResponseIdentifier']),\
                    bqs.getDistLambda(opsensory['Location'], BQSDistance)
                ])
                if results:
                    opsensory['XVel'] = -opsensory['XVel']
                    opsensory['Location'] = Geo.addLocations((opsensory['XVel'], opsensory['YVel']), opsensory['Location']) 
            else:
                opsensory['NoBounceTime'] -= 1
            if isNew:
                if opsensory['Direction'] < 0:
                    opsensory['XVel'] = -opsensory['XVel']
                if opsensory['Direction'] != 0:
                    opsensory['Location'] = Geo.addLocations((2*opsensory['XVel'], opsensory['YVel']), opsensory['Location']) 
                    ret.append(opsensory)
            else:
                opsensory['Location'] = Geo.addLocations((opsensory['XVel'], opsensory['YVel']), opsensory['Location']) 
                ret.append(opsensory)
        return (ret, []) 

    def insertVelIfMissing(self, data):
        isNew = False
        if not 'XVel' in data:
            data['XVel'] = self['XVel']
            isNew = True
        if not 'YVel' in data:
            data['YVel'] = self['YVel']
            isNew = True
        return isNew

