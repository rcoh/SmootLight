from operationscore.PixelMapper import *
import numpy

# In XML config, set Intensity to some float.

class PedMapper(PixelMapper):
    def mappingFunction(self, inp, screen):
        # inp is a dictionary of {sensor location: intensity}
        result = numpy.zeros(len(screen))
        for loc in inp:
            result += inp[loc] / sum(square(loc-screen.locs),-1)
        return numpy.minimum(1, sqrt(result) * self.Intensity)
