from operationscore.PixelMapper import *

class FunctionMapper(PixelMapper):
    def mappingFuncion(self, loc, screen):
        if not hasattr(self, 'func'):
            self.func = eval('lambda x,y:' + self.Function)
        return self.func(screen.locs[:,0], screen.locs[:,1])
