from operationscore.PixelMapper import *
import numpy

# turn on all pixels within a square of side length 2*dist centered at
# loc (so edges are orthogonal)

class SquareBlobMapper(PixelMapper):
    def mappingFunction(self, inp, screen):
        # inp is a tuple (location, distance)
        return numpy.amax(abs(screen.locs - inp[0]), -1) < inp[1]
