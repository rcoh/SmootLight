from operationscore.Behavior import *
from pixelevents.SynchTestEvent import *
import pdb
class SynchTest(Behavior):
    def behaviorInit(self):
        self.rendered = False
    def processResponse(self, sensorInputs, recurs):
        if not self.rendered:
            self.rendered = True
            print 'here1'
            return ([{'Location':1, 'PixelEvent':SynchTestEvent({'Color':(255,0,0)})}], [])
        return ([], []) 
