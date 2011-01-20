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
            if bestPixel != None:
                return [(bestPixel,1)]
            else:
                return [] 
        else:
            #{x}>5,{y}<k
            #TODO: we should probably encapsulate this somewhere
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

