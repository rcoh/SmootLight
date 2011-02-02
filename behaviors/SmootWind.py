from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import random

class SmootWind(Behavior):
    def behaviorInit(self):
        self.mapper = None
        self.xFor = None

    def processResponse(self, sensorInputs, recursiveInputs):
	if self.mapper == None:
            try:
                self.mapper = compReg.getComponent('windgaussmap')
            except KeyError:
                pass
        if self.xFor == None:
            try:
                self.xFor = compReg.getComponent('xfor')
            except KeyError:
                pass

        for sensory in sensorInputs:
            print sensory
            # input[0] is windspeed, [1] is dir
	    if 0 in sensory and 1 in sensory:
		    windSpeed = sensory[0]
		    windDir = sensory[1]
		    #print self.mapper.argDict
		    self.mapper.argDict['Width'] = self.mapper.argDict['Width']+float(windSpeed)*2+20
		    self.xFor.argDict['ParamOp'] = self.xFor.argDict['ParamOp']+float(windSpeed)*3+10*random.random(); 
		    #print 'Width: ' + str(self.mapper.argDict['Width'])
		    #print 'xFor: ' + str(self.xFor.argDict['ParamOp'])

	    elif 'Key' in sensory:
		    if sensory['Key'] == 273:
			    self.mapper.argDict['Width'] = self.mapper.argDict['Width']+10;
			    self.xFor.argDict['ParamOp'] = self.xFor.argDict['ParamOp']+5;
		   
		    elif sensory['Key'] == 274:
			    self.mapper.argDict['Width'] = self.mapper.argDict['Width']-10;
			    self.xFor.argDict['ParamOp'] = self.xFor.argDict['ParamOp']-5;

        return (sensorInputs, recursiveInputs)
