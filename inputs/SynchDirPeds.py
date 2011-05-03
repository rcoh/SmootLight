from operationscore.Input import *
import util.ComponentRegistry as compReg
from logger import main_log
import util.TimeOps as timeOps
from operationscore.SmootCoreObject import *
import sys
import time
class SynchDirPeds(SmootCoreObject):
    def init(self):
        self.cached = []
        self.responses = []
    def processInput(self, inp):
        self.responses = inp
        self.pruneCache(self.cached)
        newCache = []
        for r in self.responses:
            bestMatch,t = self.findClosest(self.cached, r['Location'][0]) 
            r['Direction'] =  r['Location'][0]-bestMatch
            r['Velocity'] = r['Direction']/(timeOps.time()-t)
            newCache.append((r['Location'][0], r['Responding'])) 

        self.cached += newCache
        respCopy = list(self.responses)
        return respCopy 
    
    def pruneCache(self, cache):
        currentTime = timeOps.time()
        rem = []
        for l,t in cache:
            if currentTime-t > 5000:
                rem.append((l,t))
        for r in rem:
            cache.remove(r)
    def findClosest(self, cache, location):
        #TODO: numpyify
        #print len(cache)
        bestMatch = None
        bestDist = sys.maxint
        bestTime = None
        if cache == []:
            return location,timeOps.time() 
        tcache = list(cache)
        tcache.reverse()
        for x,t in tcache:
            if bestMatch == None or abs(x-location)<bestDist:
                bestDist = abs(x-location)
                bestMatch = x
                bestTime = t 
        cache.remove((bestMatch,bestTime))
        return bestMatch,t

