from operationscore.Behavior import *
from util import ComponentRegistry
from pixelevents.SingleFrameEvent import *
import random
class Warehouse(Behavior):
    def behaviorInit(self):
        self.maxX = ComponentRegistry.getComponent('Screen').size[2]
    def processResponse(self, sensors, recurs):
        if len(recurs) < 1:
            recurs.append({'Location':0, 'Thresh':.02})
        output = []
        for r in recurs:
            inc = 180 if random.random() < r['Thresh'] else 0 
            r['Location'] += inc 
            if inc > 0:
                r['Thresh'] += .01
            outDict = dict(r)
            outDict['PixelEvent'] = SingleFrameEvent({'Color':(255,255,255), 'Coefficient':.01}) 
            xThresh  = r['Location']
            outDict['Location'] = lambda x,y: (x > 0) & (x<r['Location'])
            output.append(outDict)
        return (output, recurs)

