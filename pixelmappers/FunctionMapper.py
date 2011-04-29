from operationscore.PixelMapper import *

# the location argument is a function of x and y

class FunctionMapper(PixelMapper):
    def mappingFunction(self, func, screen):
        return func(screen.locs[:,0], screen.locs[:,1])
