from operationscore.SmootCoreObject import *
import util.Geo as Geo
import pdb
class PixelAssembler(SmootCoreObject):
    def init(self):
        self.validateArgs('PixelAssembler.params')
        self.initLayout()
    def layoutFunc(self, lastLocation):
        raise NotImplementedError
    def getPixelLocations(self): #returns a complete list of locations of Pixels
        #for a strip
        locations = [self.argDict['originLocation']]
        for pixelIndex in range(self['numPixels']-1): #-1 because origin
            #already exists
            newLocation = self.layoutFunc(locations[-1]) 
            if (Geo.dist(newLocation, locations[-1]) >
                self['pixelToPixelSpacing']):
                raise Exception('Illegal pixel location.  Distance between adjacent ' 
                                + 'pixels must be less than pixelToPixelSpacing.'
                                + 'Illegal distance is between {0} and {1}'
                                .format(pixelIndex, pixelIndex+1))
            locations.append(newLocation)
        if self['Reverse']:
            locations.reverse()
        return locations
    def initLayout(self):
        pass
    def getStripArgs(self): #TODO: triage and remove
        return self.argDict
