from operationscore.PixelMapper import *
from numpy import minimum, square, sum

class PseudoGaussianMapper(PixelMapper):
    """
    <Width> -- The width of the gaussian-like surface
    <Intensity> -- Intensity of the color
    """
    def mappingFunction(self, loc, screen):
        return minimum(self.Intensity, self.Width/sum(square(screen.locs-loc),-1))
