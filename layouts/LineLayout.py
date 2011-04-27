from operationscore.PixelAssembler import *
import numpy

class LineLayout(PixelAssembler):
    """LineLayout is a layout class that makes a line of LEDs.
    In argDict, "step" is a tuple (xStep, yStep).
    "originLocation" is a tuple (x, y)."""
    def layoutFunc(self):
         return (numpy.arange(self["numPixels"])[:,None]
                 * self["step"] + self["originLocation"])[::(-1 if self["Reverse"] else 1)]
