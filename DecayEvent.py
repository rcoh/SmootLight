from PixelEvent import PixelEvent
import Util, math
class DecayEvent(PixelEvent):
    def initEvent(self):
        self.validateArgs('DecayEvent.params')
        self['Coefficient'] = abs(self['Coefficient'])
    def lightState(self,timeDelay):
        if self['DecayType'] == 'Exponential':
            decay = math.exp(timeDelay*-1*self['Coefficient'])
        if self['DecayType'] == 'Proportional':
            decay = float(self['Coefficient']) / timeDelay
        return Util.multiplyColor(self['Color'], decay)
