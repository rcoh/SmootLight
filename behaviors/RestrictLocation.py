from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Geo as Geo
import util.Strings as Strings
import random
class RestrictLocation(Behavior):
    def behaviorInit(self):
        action = self['Action']
        modifyParamArgs = {'ParamType': 'Sensor',
                'ParamName':self['ParamName'],'ParamOp':self['Action']} 
        
    def processInput(
