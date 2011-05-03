from operationscore.PixelMapper import *
from numpy import minimum, square, sum

class PseudoGaussianMapper(PixelMapper):
    """
    <Width> -- The width of the gaussian-like surface
    """
    def mappingFunction(self, loc, screen):
        return minimum(1, self.Width/sum(square(screen.locs-loc),-1))
