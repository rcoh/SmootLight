from operationscore.PixelAssembler import *
import pdb
import numpy

class ZigzagLayout(PixelAssembler):
    """ZigZagLayout is a slightly more complex layout class that makes a zig-Zag Led Pattern
    Inheriting classes must specify slowStep, fastStep, zigLength, and numPixels.
    EG: slowStep = (0,-1), fastStep = (1,0), zigLength = 4, numPixels = 12:
     O-O-O-O    
           |    Y
     O-O-O-O    |
     |          0--X
     O-O-O-O."""
    
    def layoutFunc(self):
        slow, fast = numpy.mgrid[:self["numPixels"]/self["zigLength"],
                                  :self["zigLength"]][...,None]
        fast[1::2] = fast[1::2,::-1].copy() # reverse every other zig
        print("Running layoutfunc with {0} {1}".format(slow, fast))
        return (slow*self["slowStep"] + fast*self["fastStep"]).reshape((-1,2))
