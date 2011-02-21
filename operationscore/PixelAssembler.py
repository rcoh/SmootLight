from operationscore.SmootCoreObject import *
import util.Geo as Geo
import pdb
class PixelAssembler(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelAssembler.params')
    def layoutFunc(self):
        raise NotImplementedError # subclass must do this
    def getPixelLocations(self): #returns a complete list of locations of Pixels
        locations = self.layoutFunc()
        for pixel1, pixel2 in zip(locations[:-1], locations[1:]):
            if (Geo.dist(pixel1, pixel2) > self['pixelToPixelSpacing']):
                raise Exception('Illegal pixel location.  Distance between adjacent ' 
                                + 'pixels must be less than pixelToPixelSpacing.'
                                + 'Illegal distance is between {0} and {1}'
                                .format(pixel1, pixel2))
        return locations[::-1] if self['Reverse'] else locations
    def getStripArgs(self): #TODO: triage and remove
        return self.argDict
