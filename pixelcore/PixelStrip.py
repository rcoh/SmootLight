from pixelcore.Pixel import *
import util.Strings as Strings
import util.Geo as Geo
from pixelevents.StepEvent import *
import math
import pdb
class PixelStrip:
    """Python class representing a single Pixel strip (usually 50 Pixels)"""
    
    def __init__(self, layoutEngine):
        self.initStrip(layoutEngine)
        self.argDict = layoutEngine.getStripArgs()
    
    def initStrip(self, layoutEngine):
        pixelLocations = layoutEngine.getPixelLocations()
        self.pixels = [Pixel(l) for l in pixelLocations]
    
    def __iter__(self):
        return self.pixels.__iter__()

