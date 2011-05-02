from operationscore.PixelEvent import *
from numpy import array, exp

class RiseFallEvent(PixelEvent):
    """<Duration> -- length of time between first and last light."""
    def state(self, time):
        d = self.Duration
        if time == 0: return [0, 4./d, -4./d/d], d
        return None
    
    @staticmethod
    def generate(duration):
        return RiseFallEvent({'Duration': duration})
