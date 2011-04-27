from operationscore.Behavior import *
from util import ComponentRegistry
from pixelevents.DecayEvent import *
class LayoutTest(Behavior):
    def behaviorInit(self):
        self.maxX = ComponentRegistry.getComponent('Screen').size[2]
    def processResponse(self, sensors, recurs):
        if len(recurs) < 20:
            recurs.append({'Location':0})
        output = []
        for r in recurs:
            r['Location'] += 10
            r['Location'] = r['Location'] % self.maxX
            outDict = dict(r)
            outDict['PixelEvent'] = DecayEvent({'Color':(255,255,255), 'Coefficient':.01}) 
            outDict['Location'] = lambda x,y: abs(x-r['Location']) < 30
            output.append(outDict)
        return (output, recurs)

