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
        "ls" : {
            'all' : [(2,2),(2,8), (2,14), (2,20)],
            '1'   : [(2,2)],
            '2'   : [(2,8)],
            '3'   : [(2,14)],
            '4'   : [(2,20)] },
        "ts" : {
            'all' : [(4,22), (10,22), (16,22), (22,22), (27, 22), (33, 22), (39,22), (44, 22)],
            '1'   : [(4,22)],
            '2'   : [(10,22)],
            '3'   : [(16,22)],
            '4'   : [(22,22)],
            '5'   : [(27,22)],
            '6'   : [(33,22)],
            '7'   : [(39,22)],
            '8'   : [(44,22)] },
        "rs" : {
            'all' : [(45,2), (45, 8), (45,14), (45,20)],
            '1'   : [(45,2)],
            '2'   : [(45,8)],
            '3'   : [(45,14)],
            '4'   : [(45,20)] },
        "bs" : {
            'all' : [(4,2), (10,2), (16,2), (22, 2), (27,2), (34,2), (39,2), (44,2)],
            '1'   : [(4,2)],
            '2'   : [(10,2)],
            '3'   : [(16,2)],
            '4'   : [(22,2)],
            '5'   : [(27,2)],
            '6'   : [(33,2)],
            '7'   : [(39,2)],
            '8'   : [(44,2)] },
        "wt" : {
            'all' : [(12,5), (13, 5), (16,5), (18,5), (21,5), (23,5), (26,5), (27,5), (30,5), (34,5), (37,5)],
            '1'   : [(12,5), (13,5)],
            '2'   : [(16,5)],
            '3'   : [(18,5)],
            '4'   : [(21,5)],
            '5'   : [(23,5)],
            '6'   : [(26,5),(27,5)],
            '7'   : [(30,5)],
            '8'   : [(34,5)],
            '9'   : [(37,5)] },
        "cl" : {
            'all' : [(17,8), (21,10), (24,10), (26,12), (31,12)],
            'in'  : [(21,10),(24,10),(26,12)],
            'out' : [(17,8),(31,12)],
            '1'   : [(17,8)],
            '2'   : [(21,10)],
            '3'   : [(24,10)],
            '4'   : [(26,12)],
            '5'   : [(31,12)] },
        "c5" : {
            'all' : [(6,17), (11,17), (15,17), (19,17), (22, 17), (27,17), (33,16), (34, 16), (38,17), (42,17)],
            'con' : [(6,17), (11,17), (15,17), (19,17), (22, 17), (27,17)],
            'five': [(33,16), (34, 16), (38,17), (42,17)],
            '1'   : [(6,17)],
            '2'   : [(11,17)],
            '3'   : [(15,17)],
            '4'   : [(19,17)],
            '5'   : [(22,17)],
            '6'   : [(27,17)],
            '7'   : [(33,16)],
            '8'   : [(34,16)],
            '9'   : [(38,17)],
            '10'  : [(42,17)] },
        }

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
            #pixel locs
            eventLocSplit = eventLocation.split('@')
            if len(eventLocSplit) == 2:
                [eventLocation, signPart] = eventLocSplit
                signParts = signPart.split('.')
                pixelLocs = signPosition[signParts[0]][signParts[1]]
                screen = [p for p in screen if (p.location in pixelLocs)]
                
                
            #{x}>5,{y}<k
            ret = []
            eventLocation = eventLocation.replace('{x}', 'pixel.location[0]')
            eventLocation = eventLocation.replace('{y}', 'pixel.location[1]')
            if len(eventLocation) > 0:
                conditions = eventLocation.split(',')
                conditionLambdas = [eval('lambda pixel:'+condition) for condition in conditions]
            else:
                conditionLambdas = []
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

