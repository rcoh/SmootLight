from operationscore.Behavior import *
import util.Strings as Strings
from logger import main_log
class AddPixelEvent(Behavior):
    """AddPixelEvent is a behavior to append an arbitrary PixelEvent to a behavior response.  The
    classname of the PixelEvent should be specified in the Class field of Args.  All arguments normally
    passed to the PixelEvent should also be specified in Args."""
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
            if 'PixelEvent' in sensory:
                ret.append(sensory)
            else:
                outDict = {}
                outDict[Strings.LOCATION] = sensory[Strings.LOCATION]
                settingsDict = dict(self.argDict)
                settingsDict['Color'] = sensory['Color']
                outDict['PixelEvent'] = self.eventGenerator(settingsDict)
                ret.append(outDict)
        return (ret, recurses)
