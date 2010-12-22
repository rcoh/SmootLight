from operationscore.PixelMapper import *
import util.Geo as Geo
class GaussianMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        returnPixels = [] #TODO: consider preallocation and trimming
        [x,y] = eventLocation
        for (x,pixel) in screen.pixelsInRange(x-self['CutoffDist'], \
                x+self['CutoffDist']):
            pixelDist = Geo.dist(pixel.location, eventLocation)
            if pixelDist < self['CutoffDist']:
                w = Geo.gaussian(pixelDist, self['Height'], 0, self['Width'])
                returnPixels.append((pixel, w))
        return returnPixels
