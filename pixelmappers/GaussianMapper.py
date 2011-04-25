from operationscore.PixelMapper import *
from numpy import exp, square, sum

class GaussianMapper(PixelMapper):
    """GaussianMapper is a PixelMapper which weights pixels around an event proportional to a
    gaussian surface.  Specify:
    <Height> -- The height of the gaussian surface
    <Width> -- The width of the gaussian surface
    """
    def mappingFunction(self, loc, screen):
        h, w = self.Height, self.Width
        return h * exp(-sum(square(screen.locs-loc),-1)/2/w/w)
