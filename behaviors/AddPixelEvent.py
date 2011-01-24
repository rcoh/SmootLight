from operationscore.Behavior import *
import util.Strings as Strings
from logger import main_log
class AddPixelEvent(Behavior):
    def behaviorInit(self):
        [module, className] = self['Class'].split('.')
        try:
            exec('from ' + module+'.'+className + ' import *', globals())
        except Exception as inst:
            main_log.error('Error importing ' + module+'.'+className+ '.  Component not\
            initialized.')
            main_log.error(str(inst)) 
        self.eventGenerator = eval('lambda args:'+className+'(args)') 
        
        #^lambda function to do generate new event (takes args)
    
    def processResponse(self, sensors, recurses):
        ret = []
        for sensory in sensors:
            outDict = {}
            outDict[Strings.LOCATION] = sensory[Strings.LOCATION]
            settingsDict = dict(self.argDict)
            settingsDict['Color'] = sensory['Color']
            outDict['PixelEvent'] = self.eventGenerator(settingsDict)
            ret.append(outDict)
        return (ret, recurses)
