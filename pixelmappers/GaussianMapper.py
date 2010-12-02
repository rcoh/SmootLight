from operationscore.PixelMapper import *
import Util
class GaussianMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        returnPixels = []
        for pixel in screen:
            pixelDist = Util.dist(pixel.location, eventLocation)
            if pixelDist < self['CutoffDist']:
                w = Util.gaussian(pixelDist, self['Height'], 0, self['Width'])
                if w>1:
                    pdb.set_trace()
                returnPixels.append((pixel, w))
        return returnPixels
