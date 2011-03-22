from pixelcore.Pixel import *
from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
import util.ComponentRegistry as compReg
import util.Strings as Strings
import pdb
import numpy
from scipy.spatial import KDTree
from logger import main_log

class DummyPixel: # to be removed as soon as the rest of the code allows
    def __init__(self, screen, index):
        self.screen = screen
        self.index = index
        self.location = self.screen.locs[index]
    def state(self, currentTime=None):
        return self.screen.state[0,self.index]*255
    def processInput(*args, **kwargs): pass

class DummyPixelStrip: # to be removed as soon as the rest of the code allows
    def __init__(self, screen, indices, argDict):
        self.screen = screen
        self.indices = indices
        self.argDict = argDict
    def __iter__(self):
        for i in self.indices:
            yield self.screen.pixels[i]

class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips."""
    
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
    
    def initStrips(self, layouts):
        stripLocs = [l.layoutFunc() for l in layouts]
        index = 0
        for p, l in zip(stripLocs, layouts):
            self.pixelStrips.append(DummyPixelStrip(self, range(index, index+len(p)), l.argDict))
            index += len(p)
        self.locs = numpy.concatenate(stripLocs) # locs is an n-by-2 array of all pixel locations
        self.tree = KDTree(self.locs) # super-fast nearest neighbor lookups
        self.size = [min(self.locs[:,0]), min(self.locs[:,1]),
                     max(self.locs[:,0]), max(self.locs[:,1])]
        self.state = numpy.zeros((3, len(self), 3), dtype='float') # p[n] = c1*p[n-1] + c2
        self.pixels = [DummyPixel(self, i) for i in range(len(self))]
    
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return iter(self.pixels)
    
    #SUBVERTING DESIGN FOR EFFICIENCY 1/24/11, RCOH -- It would be cleaner to store the time on the responses
    #themselves, however, it is faster to just pass it in.
    def timeStep(self, currentTime):
        """Increments time -- This processes all queued responses, adding that to a queue that will
        be processed on the next time step."""
        newQueue = []
        self.state[0] *= self.state[1]
        self.state[0] += self.state[2]
        for responseInfo in self.responseQueue:
            result = self.processResponse(responseInfo, currentTime)
            if result: newQueue.append(result)
        self.state[0] = numpy.minimum(self.state[0], 255, self.state[0])
        self.state[0] = numpy.maximum(self.state[0], 0, self.state[0])
        self.responseQueue = newQueue

    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
    
    # depricated: just use self.size
    def getSize(self):
        return self.size
    
    #private
    def processResponse(self, responseInfo, currentTime): #we need to make a new dict for
        #each to prevent interference
        mapper = compReg.getComponent(responseInfo.get('Mapper', Strings.DEFAULT_MAPPER))
        weights = mapper.mapEvent(responseInfo['Location'], self)
        main_log.debug('Screen processing response.  {0} events generated.'.format(len(weights)))
        PixelEvent.addPixelEventIfMissing(responseInfo)
        coeffs, newEvent = responseInfo['PixelEvent'].coeffs()
        arr = coeffs[:, None] * responseInfo['PixelEvent'].Color/255
        for (index, weight) in weights:
            self.state[:,index] = arr * weight
        return newEvent
