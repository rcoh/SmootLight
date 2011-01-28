from operationscore.Behavior import *
import util.ComponentRegistry as compReg

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
            #print sensory
            # input[0] is windspeed, [1] is dir
            windSpeed = sensory[0]
            windDir = sensory[1]

            #print self.mapper.argDict
            self.mapper.argDict['Width'] = float(windSpeed) ** 3
            self.xFor.argDict['ParamOp'] = float(windSpeed) ** 2
            #print 'Width: ' + str(self.mapper.argDict['Width'])
            #print 'xFor: ' + str(self.xFor.argDict['ParamOp'])
        return (sensorInputs, recursiveInputs)
