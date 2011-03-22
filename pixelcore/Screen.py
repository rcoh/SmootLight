from pixelcore.Pixel import *
from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
import util.ComponentRegistry as compReg
import util.Strings as Strings
import pdb
import numpy
from scipy.spatial import KDTree
from logger import main_log
import time

class DummyPixelStrip: # to be removed as soon as the rest of the code allows
    def __init__(self, indices, pixels, argDict):
        self.indices = indices
        self.pixels = pixels
        self.argDict = argDict
    def __iter__(self):
        return iter(self.pixels)

class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips."""
    
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
    
    def initStrips(self, layouts):
        stripLocs = [l.layoutFunc() for l in layouts]
        pixels = [map(Pixel, s) for s in stripLocs]
        index = 0
        for p, l in zip(pixels, layouts):
            self.pixelStrips.append(DummyPixelStrip(range(index, index+len(p)), p, l.argDict))
            index += len(p)
        self.locs = numpy.concatenate(stripLocs) # locs is an n-by-2 array of all pixel locations
        self.tree = KDTree(self.locs) # super-fast nearest neighbor lookups
        self.size = [min(self.locs[:,0]), min(self.locs[:,1]),
                     max(self.locs[:,0]), max(self.locs[:,1])]
        self.pixels = numpy.concatenate(pixels)
    
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return iter(self.pixels)
    
    #SUBVERTING DESIGN FOR EFFICIENCY 1/24/11, RCOH -- It would be cleaner to store the time on the responses
    #themselves, however, it is faster to just pass it in.
    def timeStep(self, currentTime):
        """Increments time -- This processes all queued responses, adding that to a queue that will
        be processed on the next time step."""
        tempQueue = list(self.responseQueue)
        self.responseQueue = []
        for response in tempQueue:
            self.processResponse(response, currentTime)
    
    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
        
    # depricated: just use self.size
    def getSize(self):
        return self.size
        
    #private
    def processResponse(self, responseInfo, currentTime): #we need to make a new dict for
        #each to prevent interference
        if type(responseInfo) != type(dict()):
            pass
        if 'Mapper' in responseInfo:
            mapper = compReg.getComponent(responseInfo['Mapper']) 
        else:
            mapper = compReg.getComponent(Strings.DEFAULT_MAPPER)
        weights = mapper.mapEvent(responseInfo['Location'], self)
        main_log.debug('Screen processing response.  {0} events generated.'.format(len(weights)))
        PixelEvent.addPixelEventIfMissing(responseInfo)
        for (index, weight) in weights:
            self.pixels[index].processInput(responseInfo['PixelEvent'], 0,weight, currentTime) #TODO: z-index
