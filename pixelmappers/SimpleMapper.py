from operationscore.PixelMapper import *
import numpy

class SimpleMapper(PixelMapper):
    """SimpleMapper is a PixelMapper which maps events to the nearest Pixel."""
    def mappingFunction(self, loc, screen):
        result = numpy.zeros(len(screen))
        result[numpy.argmin(numpy.sum(numpy.square(loc-screen.locs),-1))] = 1
        return result
