from operationscore.Input import *
import util.ComponentRegistry as compReg
import thread
from logger import main_log
import util.TimeOps as timeOps
import sys
import time
class DirectionalPedestrians(Input):
    def inputInit(self):
        self.lock = thread.allocate_lock()
        self.responses = []
        self.boundToInput = self.makeListener()
        self.cached = [] 
    def makeListener(self):
        try:
            compReg.getLock().acquire()
            compReg.getComponent(self['LocSensorId']).addListener(self)
            compReg.getLock().release()
            return True
        except Exception as ex:
            compReg.getLock().release()
            return False

    def sensingLoop(self):
        self.pruneCache(self.cached)
        if not self.boundToInput:
            self.boundToInput = self.makeListener()
        newCache = []
        for r in self.responses:
            bestMatch,t = self.findClosest(self.cached, r['Location'][0]) 
            r['Direction'] =  r['Location'][0]-bestMatch
            r['Velocity'] = r['Direction']/(timeOps.time()-t)
            newCache.append((r['Location'][0], r['Responding'])) 

        self.cached += newCache
        self.respond(self.responses)
        self.responses = []
        print 'cachesize',len(self.cached)
    
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
        if cache:
            print 'nonempty cache'
        return bestMatch,t

    def processResponse(self, sensorDict, eventDict):
        self.responses += eventDict
