from operationscore.Behavior import * 
from logger import main_log
#import util.ColorOps as color 
import colorsys
import pdb
class MrmrSetColor(Behavior):   
    def behaviorInit(self):
        self.h=0
        self.s=0
        self.v=0
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for data in sensorInputs:
            if data['Path'].find('horizontal') != -1:
                self.h = data['Value'] / 2.78
            elif data['Path'].find('vertical') != -1:
                self.s = data['Value'] / 1000.0
            else:
                main_log.error('Sensor Inputs: ' + str(sensorInputs))
        ret.append({'Color':[i*255 for i in colorsys.hsv_to_rgb(self.h,self.s,self.v)]})
        return (ret, [])
