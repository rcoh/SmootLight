from SmootCoreObject import SmootCoreObject
import Util
import pdb
class LayoutEngine(SmootCoreObject):
    def init(self):
        self.validateArgs('LayoutEngine.params')
        self.initLayout()
    def layoutFunc(self, lastLocation): #Must be defined by inheriting class.
        #Returns tuple pair (x,y)
        pass
    def getPixelLocations(self): #returns a complete list of locations of Pixels
        #for a strip
        locations = [self.argDict['originLocation']]
        for pixelIndex in range(self['numPixels']-1): #-1 because origin
            #already exists
            newLocation = self.layoutFunc(locations[-1]) 
            if newLocation == None:
                raise Exception('Location cannot be null.  layoutFunc not \
                defined or improperly defined.')
            if Util.dist(newLocation, locations[-1]) > \
                    self['pixelToPixelSpacing']:
                        raise Exception('Illegal pixel location.  Distance \
                        between adjacent pixels must be less than \
                        pixelToPixelSpacing.')
            locations.append(newLocation)
        return locations
    def initLayout(self):
        pass
    def getStripArgs(self): #TODO: triage and remove
        return self.argDict
