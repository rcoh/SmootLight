from operationscore.SmootCoreObject import *
import pdb
class PixelMapper(SmootCoreObject):
    def init(self):
        self.mem = {} #Dictionary of all seen events
        self.totalCalls = 0
        self.cachehits = 0
    def mapEvent(self, eventLocation, screen):
        self.totalCalls += 1
        if self.totalCalls % 100 == 0:
            print self['Id'], self.cachehits / float(self.totalCalls)
        if eventLocation in self.mem:
            self.cachehits += 1
            return self.mem[eventLocation]
        else:
            self.mem[eventLocation] = self.mappingFunction(eventLocation, screen)
            return self.mem[eventLocation]
    #Takes a Screen and returns a list of tuples
    #(pixel, weight), with the sum of weights = 1
    #TODO: consider abstracting away from pixels
    def mappingFunction(self,eventLocation, screen):
        pass
