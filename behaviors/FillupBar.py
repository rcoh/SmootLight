from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class FillupBar(Behavior):
    def behaviorInit(self):
        compReg.getLock().acquire()
        self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
        compReg.getLock().release()

    def processResponse(self, inputs, recurs):
        if not recurs:
            if not self['Side']:
                side = 'left'
            else:
                side = self['Side']
            if side == 'left':
                return ([{'Location':((self.minX, 0), 10)}], [{'a':True}])
            else:
                return ([{'Location':((self.maxX, 0), 10)}], [{'a':True}])
        else:
            return ([],[{'a':True}])
        #ret = []
        #inputs = list(inputs)
        #for inputset in inputs:
        #    inputset = dict(inputset)
        #    #Expecting SquareBlobMapper: ((x,y), distance)
        #    inputset['Location'] = ((inputset['Location'][0], 0), 10)
        #    ret.append(inputset)
        #return (ret, [])

