from operationscore.PixelMapper import *
import util.Geo as Geo
import sys
class SimpleMapper(PixelMapper):
    """SimpleMapper is a PixelMapper which maps events to the nearest Pixel.  It also supports
    strings of the form:
    {x}>5, {y}<10, {x}*{y}<{x}, etc. (Conditons, separated by commas.  and and or may also be
    used)."""
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
            if bestPixel != None:
                return [(bestPixel,1)]
            else:
                return [] 
        else:
            #{x}>5,{y}<k
            ret = []
            eventLocation = eventLocation.replace('{x}', 'pixel.location[0]')
            eventLocation = eventLocation.replace('{y}', 'pixel.location[1]')
            conditions = eventLocation.split(',')
            conditionLambdas = [eval('lambda pixel:'+condition) for condition in conditions]
            for pixel in screen:
                try:
                    pixelValid = True
                    for p in conditionLambdas:
                        if p(pixel) == False:
                            pixelValid = False
                            continue
                    if pixelValid:
                        ret.append((pixel, 1))
                except Exception as exp:
                    raise Exception('Bad event condition')
            return ret

