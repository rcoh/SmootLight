from operationscore.PixelEvent import *
import Util, math
class DecayEvent(PixelEvent):
    def initEvent(self):
        self.validateArgs('DecayEvent.params')
        self['Coefficient'] = abs(self['Coefficient'])
    def state(self,timeDelay):
        if self['DecayType'] == 'Exponential':
            decay = math.exp(timeDelay*-1*self['Coefficient'])
        if self['DecayType'] == 'Proportional':
            decay = float(self['Coefficient']) / timeDelay
        color = Util.multiplyColor(self['Color'], decay)
        return color if sum(color) > 5 else None
    @staticmethod
    def generate(decayType, coefficient, color):
        args = {'DecayType': decayType, 'Coefficient':coefficient, 'Color':color}
        return DecayEvent(args)
