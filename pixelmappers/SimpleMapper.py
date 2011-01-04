from operationscore.PixelMapper import *
import util.Geo as Geo
import sys
class SimpleMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        if type(eventLocation) == type(tuple()):
            bestDist = sys.maxint 
            bestPixel = None
            [x,y] = eventLocation
            for (x,pixel) in screen.pixelsInRange(x-self['CutoffDist'], \
                    x+self['CutoffDist']):
                pixelDist = Geo.dist(pixel.location, eventLocation)
                if pixelDist < bestDist:
                    bestPixel = pixel
                    bestDist = pixelDist
            return [(bestPixel,1)]
        elif type(type(str)):
            #[{x}>5,{y}<k]
            #TODO: we should probably encapsulate this somewhere
            ret = []
            eventLocation = eventLocation.replace('{x}', 'pixel.location[0]')
            eventLocation = eventLocation.replace('{y}', 'pixel.location[1]')
            for pixel in screen:
                try:
                    preValid = eval(eventLocation)
                    pixelValid = sum(preValid) == len(preValid) #TODO: some
                    #optimizations possible.  This might be slow in the long run
                    if pixelValid:
                        ret.append((pixel, 1))
                except Exception as exp:
                    raise Exception('Bad event condition')
            return ret

