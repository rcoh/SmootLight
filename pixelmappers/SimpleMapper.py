from operationscore.PixelMapper import *
import numpy
square = numpy.square
class SimpleMapper(PixelMapper):
    """SimpleMapper is a PixelMapper which maps events to the nearest Pixel."""
    def mappingFunction(self, loc, screen):
        result = numpy.zeros(len(screen))
        if loc == 'True' or loc == True:
            result[:] = 1
        else:    
            result[numpy.argmin(sum(square(loc-screen.locs),-1))] = 1
        return result
