from operationscore.Behavior import * 
from logger import main_log
#import util.ColorOps as color 
import colorsys
from numpy import array
import pdb
import util.ComponentRegistry as compReg

speedfactor = 15
vel_decay = .00

def constrainLocation(v,c):
    if v[0] > c[0]:
        v[0] = c[0]
    elif v[0]<0:
        v[0] = 0
    
    if v[1] > c[1]:
        v[1] = c[1]
    elif v[1]<0:
        v[1] = 0

    return v

class ControllerOSC(Behavior):   
    def behaviorInit(self):
        self.xy = array((0,0))
        self.v_xy = array((0,0))
        self.v_decay = vel_decay

        self.start_hsv = [0,1,1] 
        self.dest_hsv = [0,1,1] 
        self.ssize = compReg.getComponent('Screen').getSize()[-2:] #896 x 310
    
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        if sensorInputs:
            data = sensorInputs[-1]#for data in sensorInputs:
            if data['Path'] == '/sixaxis/xy':
                #try:
                    x = data['Value'][0]
                    y = data['Value'][1]
                    main_log.error(str(x))
                    if y < 0:
                        self.start_hsv[1] = 1.0+y #s
                    else:
                        self.start_hsv[2] = 1.0-y
                    self.start_hsv[0] = (x+1) * 180.0  
            elif data['Path'] == '/sixaxis/lrud':
                val=data['Value']
                vy = val[3]-val[2]
                vx = val[1]-val[0] 
                #pdb.set_trace()
                #self.v_xy = (val[1]*ssize[0], (1.0-val[0])*ssize[1])
                self.v_xy = array((vx, vy)) * speedfactor
            else:
                main_log.error('Sensor Inputs: ' + str(sensorInputs))
        self.xy = self.xy + self.v_xy
        constrainLocation(self.xy,self.ssize)
        self.v_xy -= self.v_decay
        if self.v_xy[0] < 0:
            self.v_xy[0] = 0
        if self.v_xy[1] < 0:
            self.v_xy[1] = 0
        ret.append({'Color':[i*255 for i in colorsys.hsv_to_rgb(*self.start_hsv)],'Location':(int(self.xy[0]), int(self.xy[1]))})
    
        return (ret, [])
