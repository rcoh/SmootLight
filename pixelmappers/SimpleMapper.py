from operationscore.PixelMapper import *
import util.Geo as Geo
import math
import sys
class SimpleMapper(PixelMapper):
    """SimpleMapper is a PixelMapper which maps events to the nearest Pixel.  It also supports
    strings of the form:
    {x}>5, {y}<10, {x}*{y}<{x}, etc. (Conditions, separated by commas.  Standard python syntax such
    as and and or may also be
    used).  You may use 'math.' functions such as math.sqrt, etc.  It also accepts lists of strings"""
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
            if not isinstance(eventLocation, list):
                eventLocation = eventLocation.replace('{x}', 'pixel.location[0]')
                eventLocation = eventLocation.replace('{y}', 'pixel.location[1]')
                conditions = eventLocation.split(',')
            else:
                conditions = eventLocation #TODO: check for lists of strings
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
                    import pdb; pdb.set_trace()
                    raise Exception('Bad event condition')
            return ret

