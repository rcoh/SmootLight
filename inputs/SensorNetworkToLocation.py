"""SensorNetworkToLocation converts data from a sensor network in terms of ids into their actual
locations.
Params:
<SensorId> -- the cid of the component generating raw sensor data -- Note that this component may
need to be below that component in the XML
<SensorSpacing> -- sensors location = int(id)*SensorSpacing """
from operationscore.Input import *
import util.ComponentRegistry as compReg
import thread
class SensorNetworkToLocation(Input):
    def inputInit(self):
        print 'initializing'
        self.lock = thread.allocate_lock()
        self.responses = []
        self.boundToInput = self.makeListener() 
    def makeListener(self):
        try:
            compReg.getLock().acquire()
            compReg.getComponent(self['SensorId']).addListener(self)
            compReg.getLock().release()
            print 'added'
            return True
        except Exception as ex:
            compReg.getLock().release()
            print ex
            print 'comp not initialized'
            return False
    
    def sensingLoop(self):
        if not self.boundToInput:
            self.boundToInput = self.makeListener()
        for r in self.responses:
            r['Location'] = (int(r['SensorId'])*self['SensorSpacing'], 100)
        if self.responses:
            print self.responses
            self.respond(self.responses)
        self.responses = []
    def processResponse(self, sensorDict, eventDict):
        self.responses += eventDict
