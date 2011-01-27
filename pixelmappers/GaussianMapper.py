from operationscore.PixelMapper import *
import util.Geo as Geo
class GaussianMapper(PixelMapper):
    """GaussianMapper is a PixelMapper which weights pixels around an event proportional to a
    gaussian surface.  Specify:
    <Height> -- The height of the gaussian surface
    <Width> -- The width of the gaussian surface
    <MinWeight> -- the minimum weight event that can be returned
    <CutoffDist> -- the maximum radius considered
    """

    def mappingFunction(self, eventLocation, screen):
        returnPixels = [] 
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
