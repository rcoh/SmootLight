from operationscore.PixelMapper import *
import util.Geo as Geo
from numpy import matrix, array

class DiffuserMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        result = []
        for strip in screen.pixelStrips:
            try:
                basis = [strip.argDict["step"], strip.argDict['diffuser']]
            except:
                raise (NotImplementedError,
                       'DiffuserMapper was given undiffused pixels')
            for i, p in zip(strip.indices, strip.pixels):
                offset = eventLocation - p.location
                dist, height = array(offset * matrix(basis)**-1)[0]
                if abs(dist) < .5:
                    if self['RevLen'] <= height <= 0:
                        result.append((i, 1 + height/self['RevLen']))
                    elif 0 <= height <= self['FwdLen']:
                        result.append((i, 1 - height/self['FwdLen']))
        return result
