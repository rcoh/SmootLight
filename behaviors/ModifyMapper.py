from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json

class ModifyMapper(Behavior):
    def behaviorInit(self):
        self.mapper = None
        
    def processResponse(self, sensorInputs, recursiveInputs):
        if self.mapper == None:
            try:
                compReg.getLock().acquire()
                self.mapper = compReg.getComponent(self.argDict['MapperId'])
                compReg.getLock().release()
            except KeyError:
                print 'Error when ModifyMapper'
                pass

        paramChange = json.loads(self.argDict['ParamChange'])
        print self.mapper.argDict['CutoffDist']
        for k,v in paramChange.items():
            self.mapper.argDict[k] += v
        
        return (sensorInputs, recursiveInputs)
