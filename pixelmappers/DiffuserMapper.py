from operationscore.PixelMapper import *
import util.Geo as Geo
from numpy import matrix, array

class DiffuserMapper(PixelMapper):
    def mappingFunction(self, loc, screen):
        result = []
        for strip in screen.strips:
            try:
                basis = [strip.step, strip.diffuser]
            except:
                raise (NotImplementedError, 'DiffuserMapper was given undiffused pixels')
            for i in strip.indices:
                offset = loc - screen.locs[i]
                dist, height = array(offset * matrix(basis)**-1)[0]
                if abs(dist) < .5:
                    if self['RevLen'] <= height <= 0:
                        result.append((i, 1 + height/self['RevLen']))
                    elif 0 <= height <= self['FwdLen']:
                        result.append((i, 1 - height/self['FwdLen']))
        return result
