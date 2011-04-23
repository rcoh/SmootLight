from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json

class ModifyMapper(Behavior):
    def behaviorInit(self):
        self.mapper = None
        
    def processResponse(self, sensorInputs, recursiveInputs):
        self.mapper = compReg.getComponent(self.argDict['MapperId'])        
        print 'CutoffDist: ' + str(self.mapper.argDict['CutoffDist']) + ', Width: ' + str(self.mapper.argDict['Width'])

        paramChange = json.loads(self.argDict['ParamChange'])
        for k,v in paramChange.items():
            #print str(k) + ': ' + str(v)
            self.mapper.argDict[k] += v
        
        return (sensorInputs, recursiveInputs)
