from operationscore.Behavior import *
import util.ComponentRegistry as compReg
from behaviors.ModifyParam import *
import util.Geo as Geo
import util.Strings as Strings
import random
class LocationBasedEvent(Behavior):
    """LocationBasedEvent is a Behavior which does an action -- A ModifyParam, actually, when a certain
    location based condition is met.  It takes arguments as follows:

    <Action> -- Operation to perform, using ModifyParam syntax.  Use {val} to reference the variable
    specified by ParamName.
    <ParamName> -- the name of the parameter to modify.
    <LocationRestriction> -- either a tuple of (xmin,ymin,xmax,ymax) or a python-correct conditional.  Use {x} and
    {y} to reference x and y.  Use &lt; and &gt; to get < and > in XML.  EG:
    <LocationRestriction>{x}&lt;0 or {x}&gt;800</LocationRestriction>"""

    def behaviorInit(self):
        modifyParamArgs = {'ParamType': 'Sensor',
                'ParamName':self['ParamName'],'ParamOp':self['Action']} 
        self.locBounds = self['LocationRestriction']
        self.paramModifier = ModifyParam(modifyParamArgs) 
        xmin,ymin,xmax,ymax = compReg.getComponent('Screen').getSize()
        replacementDict = {'{x}':'l[0]','{y}':'l[1]', '{xmin}':str(xmin), '{xmax}':str(xmax),
                           '{ymin}':str(ymin),'{ymax}':str(ymax)}
        if isinstance(self.locBounds, str):
            for key in replacementDict:
                self.locBounds = self.locBounds.replace(key, replacementDict[key])
            self.locEval = eval('lambda l:'+self.locBounds)
        elif isinstance(self.locBounds, tuple):
            if len(self.locBounds) != 4:
                raise Exception('Must be in form (xmin,yin,xmax,ymax)')
            else:
                self.locEval = lambda l:Geo.pointWithinBoundingBox(l,\
                        self.LocBounds)
    def recalc(self):
        self.locBounds = self['LocationRestriction']
        xmin,ymin,xmax,ymax = compReg.getComponent('Screen').getSize()
        replacementDict = {'{x}':'l[0]','{y}':'l[1]', '{xmin}':str(xmin), '{xmax}':str(xmax),
                           '{ymin}':str(ymin),'{ymax}':str(ymax)}
        if isinstance(self.locBounds, str) or isinstance(self.locBounds, unicode):
            for key in replacementDict:
                self.locBounds = self.locBounds.replace(key, replacementDict[key])
            self.locEval = eval('lambda l:'+self.locBounds)
        elif isinstance(self.locBounds, tuple):
            if len(self.locBounds) != 4:
                raise Exception('Must be in form (xmin,yin,xmax,ymax)')
            else:
                self.locEval = lambda l:Geo.pointWithinBoundingBox(l,\
                        self.LocBounds)

    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for data in sensorInputs:
            if self.locEval(data['Location']):
                (dataOut, recur) = self.paramModifier.immediateProcessInput([data], [])
                #behaviors expect lists ^[]
                ret += dataOut
            else:
                ret.append(data)
        return (ret, [])


