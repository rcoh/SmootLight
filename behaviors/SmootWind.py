from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import random

class SmootWind(Behavior):
    def behaviorInit(self):
        self.mapper = None
        self.xymove = None

    def processResponse(self, sensorInputs, recursiveInputs):        
	if self.mapper == None:
            try:
                self.mapper = compReg.getComponent('windgaussmap')
            except KeyError:
                pass
        if self.xymove == None:
            try:
                self.xymove = compReg.getComponent('xymove')
            except KeyError:
                pass

        outs = []
        for sensory in sensorInputs:
            #print sensory
            # input[0] is windspeed, [1] is dir
            if 'WindSpeed' in sensory and 'WindDir' in sensory:
                windSpeed = sensory['WindSpeed']
                windDir = sensory['WindDir']
                print 'speed', windSpeed
                print 'dir', windDir
                #self.mapper.Width = float(windSpeed)*2+15
                sensory['XVel'] = float(windSpeed)+10*random.random()
                sensory['YVel'] = float(windSpeed)/3.*random.uniform(-1,1)
                #self.xymove.XStep = float(windSpeed)+10*random.random();
                #self.xymove.YStep = float(windSpeed)/3.*random.uniform(-1,1); 
                #print 'Width: ' , self.mapper.Width
                #print 'xymove: (' , self.xymove.XStep, ', ', self.xymove.YStep, ')'
            else:
                outs.append(sensory)
        return (outs, [])
