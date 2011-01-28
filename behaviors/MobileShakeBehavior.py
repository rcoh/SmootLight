from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.Strings as Strings

class MobileShakeBehavior(Behavior):
    def behaviorInit(self):
        self.mapper = None
        
    def processResponse(self, sensorInputs, recursiveInputs):
        if self.mapper == None:
            try:
                self.mapper = compReg.getComponent('mobilegaussmap')
            except KeyError:
                pass

        #print sensorInputs
        for sInput in sensorInputs:
            if 'Shake' in sInput and sInput['Shake'] == 1:
                #print 'increase!'
                self.mapper.argDict['Width'] += 30
                #self.mapper.argDict['CutoffDist'] += 20                
                sInput['Shake'] = 0
                print 'Width:' + str(compReg.getComponent('mobilegaussmap').argDict['Width'])
                #print 'CutoffDist: '+ str(compReg.getComponent('mobilegaussmap').argDict['CutoffDist'])
                
        return (sensorInputs, recursiveInputs)
