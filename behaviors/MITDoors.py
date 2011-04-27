from operationscore.Behavior import *
import math
import util.ComponentRegistry as compReg
class MITDoors(Behavior):
    """MITDoors is a case-specific behavior to map keypresses to specific locations.  Written for
    Kuan 1/26/11 by RCOH"""

    def behaviorInit(self):
        self.keymapping = {'q':[2,19], 'w':[22,36], 'e':[37,49], 'r':[52,69], 't':[76,91], 'y':[94,105],
        'u':[106,117], 'i':[123,154], 'o':[158,161], 'p':[164,167], '[':[172,184]}
        screenWidth = compReg.getComponent('Screen').size[2] #(minx, miny,maxx, maxy)
        maxKey = max([max(self.keymapping[v]) for v in self.keymapping])
        mult = screenWidth / float(maxKey)
        for k in self.keymapping:
            self.keymapping[k] = [int(val*mult) for val in self.keymapping[k]]
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for data in sensorInputs:
            key = chr(data['Key'])
            if key in self.keymapping:
                bounds = self.keymapping[key]
                data = dict(data)
                data['Left'], data['Right'] = bounds 
                data['Bottom'] = self['Bottom']
                data['Location'] = (sum(bounds) / 2., self['Bottom'])
                data['Oscillate'] = False
                ret.append(data)
        return (ret, [])
