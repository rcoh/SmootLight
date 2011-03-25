from operationscore.PixelEvent import *
from operationscore.PixelMapper import *
from util import Strings, ComponentRegistry
import numpy
from scipy.spatial import KDTree
from logger import main_log
from itertools import izip

class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips."""
    
    def __init__(self):
        self.responseQueue = []
        self.pixelStrips = []
    def getSize(self):
        return self.size
    def initStrips(self, stripLayouts):
        self.strips = stripLayouts # to do: turn layout into a hybrid pixelstrip-ish object
        self.locs = numpy.concatenate([s.layoutFunc() for s in self.strips])
        self.tree = KDTree(self.locs) # super-fast nearest neighbor lookups
        self.size = [min(self.locs[:,0]), min(self.locs[:,1]),
                     max(self.locs[:,0]), max(self.locs[:,1])]
        self.state = numpy.zeros((3, len(self), 3), dtype='float') # p[n] = c1*p[n-1] + c2
        # still need access to pixel strips for diffuser and power supply information
        indices = numpy.cumsum([0] + [s.numPixels for s in self.strips])
        for strip, i1, i2 in zip(self.strips, indices[:-1], indices[1:]):
            strip.indices = range(i1, i2) # for iteration by strip-aware mappers
            strip.values = self.state[0, i1:i2] # for quick access by hardware renderer
    
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return izip(self.locs, self.state[0])
    
    def timeStep(self, currentTime):
        """Increments time -- This processes all queued responses, adding that to a queue that will
        be processed on the next time step."""
        newQueue = []
        self.state[0] *= self.state[1] # Process existing state
        self.state[0] += self.state[2] # Process existing state
        self.state *= 0 < self.state[0] # Zero out dead events
        for responseInfo in self.responseQueue:
            result = self.processResponse(responseInfo, currentTime)
            if result: newQueue.append(result)
        numpy.minimum(self.state[0], 1, self.state[0]) # Limit maximum
        numpy.maximum(self.state[0], 0, self.state[0]) # Limit minumum
        self.responseQueue = newQueue # BROKEN

    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
    
    #private
    def processResponse(self, responseInfo, currentTime):
        mapper = ComponentRegistry.getComponent(responseInfo.get('Mapper', Strings.DEFAULT_MAPPER))
        weights = mapper.mapEvent(responseInfo['Location'], self)
        main_log.debug('Screen processing response.  {0} events generated.'.format(len(weights)))
        PixelEvent.addPixelEventIfMissing(responseInfo)
        coeffs, newEvent = responseInfo['PixelEvent'].coeffs()
        arr = coeffs[:, None] * responseInfo['PixelEvent'].Color/255
        for (index, weight) in weights:
            self.state[:,index] = arr * weight
        return newEvent # BROKEN
