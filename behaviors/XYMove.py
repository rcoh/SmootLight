from operationscore.Behavior import *
import util.Geo as Geo
class XYMove(Behavior):
    """XYMove is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XStep and YStep.  As XStep and YStep are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XStep> -- the starting XStep
    <YStep> -- the starting YStep
    """

    def processResponse(self, sensor, recurs):
        ret = []
        for loc in sensor:
            oploc = dict(loc)
            self.insertStepIfMissing(oploc)
            oploc['Location'] = Geo.addLocations((oploc['XStep'], oploc['YStep']), oploc['Location']) 
            ret.append(oploc)
        return (ret, []) 
    def insertVelIfMissing(self, data):
        if not 'XVel' in data:
            data['XVel'] = self['XStep']
        if not 'YVel' in data:
            data['YVel'] = self['YStep']

