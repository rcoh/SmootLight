from operationscore.Behavior import *
import util.Geo as Geo
class XYMove(Behavior):
    def processResponse(self, sensor, recurs):
        ret = []
        for loc in sensor:
            oploc = dict(loc)
            self.insertStepIfMissing(oploc)
            print oploc['YStep']
            oploc['Location'] = Geo.addLocations((oploc['XStep'], oploc['YStep']), oploc['Location']) 
            ret.append(oploc)
        return (ret, []) 
    def insertStepIfMissing(self, data):
        if not 'XStep' in data:
            data['XStep'] = self['XStep']
        if not 'YStep' in data:
            data['YStep'] = self['YStep']

