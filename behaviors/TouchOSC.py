from operationscore.Behavior import * 
from logger import main_log
#import util.ColorOps as color 
import colorsys
import pdb
import util.ComponentRegistry as compReg
class TouchOSC(Behavior):   
    def behaviorInit(self):
        self.h=0
        self.s=0
        self.v=0
        self.xy = (-1,-1)
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for data in sensorInputs:
            if data['Path'] == '/1/fader1':
                try:
                    self.h = data['Value'][0]*360.0
                except:
                    pdb.set_trace()
            elif data['Path'] == '/1/fader2':
                self.s = data['Value'][0]
            elif data['Path'] == '/1/fader3':
                self.v = data['Value'][0]
            elif data['Path'] == '/1/xy':
                val=data['Value']
                ssize = compReg.getComponent('Screen').getSize()[-2:] #896 x 310
                self.xy = (val[1]*ssize[0], (1.0-val[0])*ssize[1])
            else:
                main_log.error('Sensor Inputs: ' + str(sensorInputs))
        ret.append({'Color':[i*255 for i in colorsys.hsv_to_rgb(self.h,self.s,self.v)],'Location':self.xy})
    
        return (ret, [])
