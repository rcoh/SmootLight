from operationscore.SmootCoreObject import *
import util.TimeOps as timeOps
import random
"""
Simulates a motion sensor:
    DetectionRange
    DetectionProbability
    RefactoryTime
    DataHook
    Location
"""
class MotionSensorSimulator(SmootCoreObject):
    def init(self):
        #defaults:
        if not self['RefactoryTime']:
            self['RefactoryTime'] = 1500
        if not self['DetectionRange']:
            self['DetectionRange'] = 30
        if not self['DetectionProbability']:
            self['DetectionProbability'] = 1
        self.lastDetection = timeOps.time()-self['RefactoryTime'] 
        self.objLocHook = self['DataHook']
    
    def sensingLoop(self):
        currentTime = timeOps.time()
        dataLocs = self.objLocHook.getLocs()

        for loc in dataLocs:
            if abs(loc-self['Location']) < self['DetectionRange']:
                if random.random() < self['DetectionProbability']: #TODO: refactory time
                    self['parentScope'].processResponse({'SensorId':self['Id'],
                                                         'Responding':currentTime})

