from operationscore.PixelMapper import *
import util.Geo as Geo
import sys
class C5SignMapper(PixelMapper):
    """C5SignMapper is a modification to SimpleMapper which maps events to the
    nearest Pixel. In addtion, it also maps sign artifacts (letters, logo, etc)
    to their representative locations if given in the form "ts rs :: conditions"
    It also supports strings of the form: {x}>5, {y}<10, {x}*{y}<{x}, etc. 
    (Conditons, separated by commas.  and and or may also be used)."""

    signPosition = {
        "ls" : [(2,8), (2,14), (2,20)],
        "ts" : [(4,22), (10,22), (16,22), (22,22), (27, 22), (33, 22), (39,22),
                (44, 22)],
        "rs" : [(45,2), (45, 8), (45,14), (45,20)],
        "bs" : [(4,2), (10,2), (16,2), (22, 2), (27,2), (34,2), (39,2), (44,2)],
        "wt" : [(12,5), (13, 5), (16,5), (18,5), (21,5), (23,5), (26,5), (27,5),
                (30,5), (34,5), (37,5)],
        "cl" : [(17,8), (21,10), (24,10), (26,12), (31,12)],
        "c5" : [(6,17), (11,17), (15,17), (19,17), (22, 17), (27,17), (33,16),
                (34, 16), (38,17), (42,17)]}

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
        elif type(eventLocation) == type
        else:
            eventLocSplit = eventLocation.split(' :: ')
            if len(eventLocSplit) == 2:
                [signPart, eventLocation] = eventLocSplit
                signParts = [signPosition[x] for x in signPart.split(' ')]
                
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

