from operationscore.SmootCoreObject import *
import Util
import pdb
class PixelMapper(SmootCoreObject):
    def init(self):
        self.mem = {} #Dictionary of all seen events
    def mapEvent(self, eventLocation, screen):
        if eventLocation in self.mem:
            return self.mem[eventLocation]
        else:
            self.mem[eventLocation] = self.mappingFunction(eventLocation, screen)
            return self.mem[eventLocation]
    #Takes a Screen and returns a list of tuples
    #(pixel, weight), with the sum of weights = 1
    #TODO: consider abstracting away from pixels
    def mappingFunction(self,eventLocation, screen):
        pass
