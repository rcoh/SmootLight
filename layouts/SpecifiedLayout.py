from operationscore.PixelAssembler import *
import numpy

class SpecifiedLayout(PixelAssembler):
    """SpecifiedLayout is a class that allows precise specification of each individual LED.
    originLocation is irrelevant for this layout.
    Configure with a <Locations> tag in the args dict as follows':
    <Args>
        <Locations>
            <Loc>(1,1)</Loc>
            <Loc>(50,50)</Loc>
        </Locations>
        etc.
    </Args>
    You may put attributes on the Locs so that you don't get confused.
    """
    def layoutFunc(self):
        return numpy.array(self['Locations'])
