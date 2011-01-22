from operationscore.Behavior import *
import util.ComponentRegistry as compReg
from behaviors.ModifyParam import *
import util.Geo as Geo
import util.Strings as Strings
import random
import pdb
class RestrictLocation(Behavior):
    def behaviorInit(self):
        action = self['Action']
        modifyParamArgs = {'ParamType': 'Sensor',
                'ParamName':self['ParamName'],'ParamOp':self['Action']} 
        self.locBounds = self['LocationRestriction']
        self.paramModifier = ModifyParam(modifyParamArgs) 
        if isinstance(self.locBounds, str):
            self.locBounds = self.locBounds.replace('{x}', 'l[0]')
            self.locBounds = self.locBounds.replace('{y}', 'l[1]')
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


