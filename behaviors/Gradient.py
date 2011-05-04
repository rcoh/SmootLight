from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import math
from numpy import sign

class Gradient (Behavior):
    """Gradient draws a specified three-color gradient in a specified region.
    <Args>
        <Gradient>
            <Color> <Peak> <Width> <Min> <Max>
            ...

    Each will draw a gradient in the
    specified color which peaks with weight Max at x=xPeak and y=yPeak (if
    either is not defined, then peak is a line, not a point) which drops down
    to Min at a distance x/yWidth from the Peak."""

    def behaviorInit(self):
        self.xMin, self.yMin, self.xMax, self.yMax = \
                                        compReg.getComponent('Screen').size
        self.gradients = self['Gradient']
        if isinstance(self.gradients,dict):
            self.gradients = [self.gradients]
        self.scrwid = self.xMax - self.xMin

    def processResponse (self, inputs, state):
        outputs = []
        for gradient in self.gradients:
            width = gradient['Width'] * self.scrwid
            mincol = gradient['Min']
            height = gradient['Max'] - mincol
            offset = gradient['Peak'] * self.scrwid
            color = gradient['Color']
            if inputs:
                inp = inputs[0]
                (xLoc, yLoc) = inp['Location']

                #height is te maximum color intensity difference
                #width is self[Width] adjusted for width of screen, 
                #mincol is minumum color intensity
                #offset is the peak

                #step is the heaviside step function
                #step = lambda x: ((math.copysign(1, x)+1)/2)* height
                #wave centered at width, over the interval 0 to 1
                #wave = lambda val: -((abs(val-width))-width) * step(2*width-val)) + mincol
                #takes an location coefficient, maps it to the wave funciton
                #mapper = lambda loc,pixel: (loc + width + offset + xLoc) % scrwid
                #together, becomes
                #location = lambda x,y: wave(mapper(x, u))

                output = dict(inp)
                output['Color'] = color
                location = \
                    str(mincol) + "-(" + \
                        "(abs( (x + " + str(width + offset + xLoc) + ") % " + \
                            str(self.scrwid) + " - " + str(width) + ") / " + \
                            str(width) + " - 1) * " + \
                        "( " + str(height) + " * ((numpy.sign(" + \
                            "(2*" + str(width) + "- ((x + " + \
                                str(width + offset + xLoc) + ") % " + \
                                str(self.scrwid) + ")))+1)/2)))"
                output['Location'] = location
                outputs.append(output)
        return (outputs, state)
