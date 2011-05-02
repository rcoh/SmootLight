from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json

class ModifyMapper(Behavior):
    def behaviorInit(self):
        self.mapper = None
        
    def processResponse(self, sensorInputs, recursiveInputs):
        self.mapper = compReg.getComponent(self.argDict['MapperId'])        
        #print 'CutoffDist: ' + str(self.mapper.argDict['CutoffDist']) + ', Width: ' + str(self.mapper.argDict['Width'])
        #print 'CutoffDist: ' + str(self.mapper.CutoffDist) + ', Width: ' + str(self.mapper.Width)
        
        self.mapper.CutoffDist = self.argDict['CutoffDistChange']
        self.mapper.Width = self.argDict['WidthChange']
        
        return (sensorInputs, recursiveInputs)
