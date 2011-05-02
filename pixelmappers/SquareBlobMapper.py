from operationscore.PixelMapper import *
import numpy
import util.ComponentRegistry as compReg

# turn on all pixels within a square of side length 2*dist centered at
# loc (so edges are orthogonal)

class SquareBlobMapper(PixelMapper):
    def mappingFunction(self, inp, screen):
        if self['GrowthDirection'] != None:
            growthDirection = self['GrowthDirection']
        else:
            growthDirection = 'right'

        # inp is a tuple (location, distance)
        if growthDirection == 'right':
            return numpy.amax(screen.locs - inp[0], -1) < inp[1]
        else:
            return numpy.amax(numpy.array(zip([inp[0][0] - i[0] for i in screen.locs], [i[1] - inp[0][1] for i in screen.locs])), -1) < inp[1]
