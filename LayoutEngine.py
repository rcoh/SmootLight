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
    def getLightLocations(self): #returns a complete list of locations of lights
        #for a strip
        locations = [self.argDict['originLocation']]
        for lightIndex in range(self['numLights']-1): #-1 because origin
            #already exists
            newLocation = self.layoutFunc(locations[-1]) 
            if newLocation == None:
                raise Exception('Location cannot be null.  layoutFunc not \
                defined or improperly defined.')
            if Util.dist(newLocation, locations[-1]) > \
                    self['lightToLightSpacing']:
                        raise Exception('Illegal light location.  Distance \
                        between adjacent lights must be less than \
                        lightToLightSpacing.')
            locations.append(newLocation)
        return locations
    def initLayout(self):
        pass
    def getStripArgs(self): #TODO: triage and remove
        return self.argDict
