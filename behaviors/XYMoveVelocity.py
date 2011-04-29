from operationscore.Behavior import *
import util.Geo as Geo
import util.TimeOps as timeOps
class XYMoveVelocity(Behavior):
    """Like XY-Move, but takes XVel, YVel in units / ms
    Optional Params:
        <XVel> starting XVel
        <YVel> starting YVel
    """
    def processResponse(self, sensor, recurs):
        ret = []
        for loc in sensor:
            oploc = dict(loc)
            self.insertVelIfMissing(oploc)
            deltaT = timeOps.time()-oploc['EvalTime']
            deltaLoc = (deltaT*oploc['XVel'], deltaT*oploc['YVel'])
            #print 'diff:',deltaLoc
            oploc['Location'] = Geo.addLocations(deltaLoc, oploc['Location'])
            oploc['EvalTime'] = timeOps.time()
            ret.append(oploc)
        return (ret, [])
    def insertVelIfMissing(self, data):
        if not 'XVel' in data:
            data['XVel'] = self['XVel']
        if not 'YVel' in data:
            data['YVel'] = self['YVel']
        if data['XVel'] == None:
            data['XVel'] = 0
        if data['YVel'] == None:
            data['YVel'] = 0
        if not 'EvalTime' in data:
            data['EvalTime'] = timeOps.time()
