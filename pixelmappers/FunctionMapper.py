from operationscore.PixelMapper import *
import numpy

# the location argument is a function of x and y

class FunctionMapper(PixelMapper):
    def mappingFunction(self, func, screen):
        if isinstance(func, str):
            func = eval("lambda x,y: " + func)
        return func(screen.locs[:,0], screen.locs[:,1])
