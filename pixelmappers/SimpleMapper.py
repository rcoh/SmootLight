from operationscore.PixelMapper import *
import Util
class SimpleMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        bestDist = 10**10 #don't kill me, I'm lazy
        bestPixel = None
        for pixel in screen:
            pixelDist = Util.dist(pixel.location, eventLocation)
            if pixelDist < bestDist:
                bestPixel = pixel
                bestDist = pixelDist
        return [(bestPixel,1)]


