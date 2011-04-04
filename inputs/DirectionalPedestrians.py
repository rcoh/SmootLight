from operationscore.Input import *
import util.ComponentRegistry as compReg
import thread
from logger import main_log
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
        if not self.boundToInput:
            self.boundToInput = self.makeListener()
        newCache = []
        for r in self.responses:
            bestMatch = self.findClosest(self.cached, r['Location'][0]) 
            r['Direction'] =  r['Location'][0]-bestMatch
            newCache.append(r['Location'][0]) 

        self.cached += newCache
        self.respond(self.responses)
        self.responses = []
         
    def findClosest(self, cache, location):
        #TODO: numpyify
        bestMatch = None
        bestDist = sys.maxint
        if cache == []:
            return location 
        for x in cache:
            if bestMatch == None or abs(x-location)<bestDist:
                bestDist = abs(x-location)
                bestMatch = x
        cache.remove(bestMatch)
        return bestMatch

    def processResponse(self, sensorDict, eventDict):
        self.responses += eventDict
