from operationscore.PixelMapper import *
import Util
class SimpleMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        if type(eventLocation) == type(tuple()):
            bestDist = 10**10 #don't kill me, I'm lazy
            bestPixel = None
            for pixel in screen:
                pixelDist = Util.dist(pixel.location, eventLocation)
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
                    pixelValid = sum(eval(eventLocation)) == len(eventLocation)
                    ret.append((pixel, 1))
                except:
                    raise Exception('Bad event condition')
            return ret
