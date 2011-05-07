from operationscore.SmootCoreObject import *
from logger import main_log
import pdb
class PixelMapper(SmootCoreObject):
    """PixelMapper is the parent class for PixelMappers.  Inheriting classes should define
    mappingFunction which takes an eventLocation and a screen and returns a list of (weight, pixels).  PixelMapper
    handles caching automatically."""
    def init(self):
        self.mem = {} #Dictionary of all seen events
        self.totalCalls = 0
        self.cachehits = 0
        self['Mutable'] = {'Width' : lambda x: x<=1000 and x>=1 }
    def mapEvent(self, eventLocation, screen):
        """
        self.totalCalls += 1
        return self.mappingFunction(eventLocation, screen)
        print 'funky'
        if self.totalCalls % 100 == 0:
            main_log.info('Cache percentage for :', self['Id'], self.cachehits /\
                float(self.totalCalls))        
        if eventLocation in self.mem:
            self.cachehits += 1
            return self.mem[eventLocation]
        else:
	    # TODO: RETURN MAPPING FUNCTION DIRECTLY INSTEAD OF THE CACHED DATA
            self.mem[eventLocation] = self.mappingFunction(eventLocation, screen)
            return self.mem[eventLocation]
        """
        # DO NOT CACHE
        return self.mappingFunction(eventLocation, screen)

    #Takes a Screen and returns a list of tuples
    #(pixel, weight), with the sum of weights = 1
    def mappingFunction(self,eventLocation, screen):
        """Takes a Screen and event location and returns a list of tuples (pixel,weight) with
        sum(weights)=1"""
        raise Exception('Mapping function not defined!')
