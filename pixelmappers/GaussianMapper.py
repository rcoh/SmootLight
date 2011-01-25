from operationscore.PixelMapper import *
import util.Geo as Geo
class GaussianMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        returnPixels = [] #TODO: consider preallocation and trimming
        [x,y] = eventLocation
        potentialPixels = screen.pixelsInRange(x-self.CutoffDist, \
                x+self.CutoffDist)
        for (x,pixel) in screen.pixelsInRange(x-self.CutoffDist, \
                x+self.CutoffDist):
            pixelDist = Geo.dist(pixel.location, eventLocation)
            if pixelDist < self.CutoffDist:
                w = Geo.gaussian(pixelDist, self.Height, 0, self.Width)
                if w > self.MinWeight:
                    returnPixels.append((pixel, w))
        return returnPixels
