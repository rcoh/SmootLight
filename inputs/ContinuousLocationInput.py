import util.TimeOps as clock
import util.ComponentRegistry as compReg
import util.Strings as Strings
from operationscore.Input import *
class ContinuousLocationInput(Input):
    '''Continuously returns one of nine positions on the screen as specified by the xloc
    and yloc arguments, which can take values 'min', 'max', and 'center'. '''
    def inputInit(self):
        xvals = {}
        yvals = {}
        xvals['left'], yvals['bottom'], xvals['right'], yvals['top'] = compReg.getComponent('Screen').getSize()
        (xvals['center'], yvals['center']) = ((xvals['left']+xvals['right']) / 2, (yvals['top']+yvals['bottom']) / 2)

        self.location = (xvals[self['xloc']], yvals[self['yloc']])

    def sensingLoop(self):
        self.respond({Strings.LOCATION: self.location})
        
