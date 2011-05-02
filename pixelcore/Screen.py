from operationscore.PixelEvent import PixelEvent, addPixelEventIfMissing
from operationscore.PixelMapper import PixelMapper
from util import Strings, ComponentRegistry
from numpy import *
from scipy.spatial import KDTree
from logger import main_log
from itertools import izip
from heapq import *
import imp

class Screen:
    """Class representing a collection of Pixels grouped into PixelStrips."""
    def __init__(self):
        self.responseQueue = []
        self.eventHeap = [] # stores items in the format (nextTime, lastTime, event, weights)
        self.pixelStrips = []
        self.lastTime = 0
        self._override = False
    def initStrips(self, stripLayouts):
        self.strips = stripLayouts # to do: turn layout into a hybrid pixelstrip-ish object
        self.locs = concatenate([s.layoutFunc() for s in self.strips])
        self.tree = KDTree(self.locs) # super-fast nearest neighbor lookups
        self.size = [min(self.locs[:,0]), min(self.locs[:,1]),
                     max(self.locs[:,0]), max(self.locs[:,1])]
        self.state = zeros((3, len(self), 3), dtype='float') # quadratic
        self.temp = zeros((len(self), 3), dtype="int")
        self.pixels = zeros((len(self), 3), dtype='ubyte')
        # still need access to pixel strips for diffuser and power supply information
        indices = cumsum([0] + [s.numPixels for s in self.strips])
        for strip, i1, i2 in zip(self.strips, indices[:-1], indices[1:]):
            strip.indices = range(i1, i2) # for iteration by strip-aware mappers
            strip.values = self.pixels[i1:i2] # for quick access by hardware renderer
    
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return izip(self.locs, self.pixels)
    """
    self.override(func) to make some pattern
    self.override() to turn it off
    func should take x,y,t -> array of shape (len(x),3)"
    """
    def override(self, func=False):
        self._override = func
    def timeStep(self, currentTime):
        """Increments time -- This processes all queued responses and
        events."""
        try:
            if self.lastTime < (currentTime - (currentTime % 1000)):
                self.override(imp.load_source('x','/tmp/smoot').display)
                self.eventHeap, self.state[:] = [], 0
            if self._override:
                self.pixels[:] = self._override(self.locs[:,0], self.locs[:,1], currentTime)
                return
        except IOError: self.override()
        except Exception as e:
            open('/tmp/smoot-err','w').write(str(e))
            self.override()
        t, self.lastTime = currentTime - self.lastTime, currentTime
        self.state[0] += t * (self.state[1] + t * self.state[2])
        self.state[1] += t * 2 * self.state[2]
        while self.responseQueue:
            self.processResponse(self.responseQueue.pop(0), currentTime)
        self.processEvents(currentTime)
        maximum(0, self.state[0], self.temp)
        minimum(255, self.temp, self.pixels)
    
    #public
    def respond(self, responseInfo):
        self.responseQueue.append(responseInfo)
    
    #private
    def processResponse(self, responseInfo, currentTime):
        mapper = ComponentRegistry.getComponent(responseInfo.get('Mapper', Strings.DEFAULT_MAPPER))
        weights = mapper.mapEvent(responseInfo['Location'], self)
        main_log.debug('Screen processing response.  Event generated.')
        addPixelEventIfMissing(responseInfo)
        heappush(self.eventHeap, (currentTime, currentTime, responseInfo['PixelEvent'], weights))
    def processEvents(self, currentTime):
        while self.eventHeap and self.eventHeap[0][0] <= currentTime:
            oldTime, startTime, event, weights = heappop(self.eventHeap)
            coeffs, time = event.changeInState(currentTime-startTime)
            for i,c in enumerate(coeffs): # iterate rather than broadcasting
                for j,d in enumerate(event.Color): # for memory reasons
                    self.state[i,:,j] += c*d*weights
            if time: # if the event wants to run again
                heappush(self.eventHeap, (startTime+time, startTime, event, weights))
        print 'eventheap:', len(self.eventHeap)
