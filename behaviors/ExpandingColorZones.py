from operationscore.Behavior import *
from logger import main_log
class ExpandingColorZones(Behavior):
    def behaviorInit(self):
        self.mapping = {'r':[(132,0),(255,0,0)], 'g':[(400,0), (0,255,0)],
                'b':[(668,0),
            (0,0,255)]}
        self.mappingkey = 'KeyChar'
    def processResponse(self, sensorInputs, recursiveInputs):
        ret = []
        for data in sensorInputs:
            data = dict(data)
            if self.mappingkey in data:
                try:
                    data['Location'], data['Color'] =\
                        self.mapping[data[self.mappingkey]] 
                    ret.append(data)
                except:
                    main_log.warn('Bad mapping key.  Expanding Color Zones.')
        return (ret,[])
