from operationscore.Behavior import *
import util.ColorOps as color
import pdb
class ColorChangerBehavior(Behavior):
    """ColorChangerBehavior is a behavior for adding colors to responses.  If given no arguments, it
    will generate a random color.  If it is given a list of colors [as below] it will pick randomly
    from them.

    <ColorList>
        <Color>(255,0,0)</Color>
        <Color>(30,79,200)</Color>
    </ColorList>

    ColorList also supports specification of a single color."""

    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for sensory in sensorInputs:
            newDict = dict(sensory) 
            if self['ColorList'] != None:
                if isinstance(self['ColorList'], list):
                    newDict['Color'] = color.chooseRandomColor(self['ColorList'])  #Pick randomly
                else:
                    newDict['Color'] = self['ColorList'] #Unless there is only one
            else:
                newDict['Color'] = color.randomColor() 
            ret.append(newDict)
        return (ret, [])
