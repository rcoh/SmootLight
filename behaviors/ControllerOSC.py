from operationscore.Behavior import * 
from logger import main_log
#import util.ColorOps as color 
import colorsys
from numpy import arrray
import pdb
import util.ComponentRegistry as compReg

def constrain(v,c):
    if v[0] > c[1]:
        v[0] = c[1]
    elif v[0]<0
        v[0] = 0
    
    if v[1] > c[0]:
        v[1] = c[0]
    elif v[1]<0
        v[1] = 0

    return v

class TouchOSC(Behavior):   
    def behaviorInit(self):
        self.xy = array((0,0))
        self.v_xy = array((0,0))
        self.v_decay = .1

        self.start_hsv = (0,1,1) 
        self.dest_hsv = (0,1,1) 
    
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        if sensorInputs:
            data = sensorInputs[-1]#for data in sensorInputs:
            if data['Path'] == '/sixaxis/xy':
                try:
                    x = data['Value'][0]
                    y = data['Value'][1]
                    if y < 0:
                        self.start_hsv[1] = 1+y #s
                    else:
                        self.start_hsv[2] = y
                    self.h += x  
#self.h = x * 360.
                    
                except:
                    pdb.set_trace()
            elif data['Path'] == '/sixaxis/lrud':
                val=data['Value']
                ssize = compReg.getComponent('Screen').getSize()[-2:] #896 x 310
                vx = -val[3] if val[3] else val[2]
                vy = -val[0] if val[0] else val[1]
                #self.v_xy = (val[1]*ssize[0], (1.0-val[0])*ssize[1])
                self.v_xy = array((vx, vy))
            else:
                main_log.error('Sensor Inputs: ' + str(sensorInputs))
        self.xy = self.xy + self.v_xy
        constrain(self.xy,ssize)
        self.v_xy -= self.v_decay
        ret.append({'Color':[i*256 for i in colorsys.hsv_to_rgb(*self.start_hsv)],'Location':tuple(self.xy)})
    
        return (ret, [])
