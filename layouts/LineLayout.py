from operationscore.PixelAssembler import *
class LineLayout(PixelAssembler):
    """LineLayout is a layout class that makes a line of LEDs"""
    def layoutFunc(self, lastLocation):
        return (lastLocation[0]+self.argDict['spacing'], lastLocation[1])
