"""SensorNetworkToLocation converts data from a sensor network in terms of ids into their actual
locations.
Params:
<SensorNetworkId> -- the cid of the component generating raw sensor data -- Note that this component may
need to be below that component in the XML
<SensorSpacing> -- sensors location = int(id)*SensorSpacing 
<Y> -- the Y location specified by the user

SensorNetworkToLocation takes packets with field <SensorId>int</SensorId>.  It adds a <Location> tag
to the response which it infers from the SensorId field.

"""

#TODO: add logging
from operationscore.Input import *
import util.ComponentRegistry as compReg
import thread
from logger import main_log
class SensorNetworkToLocation(Input):
    def inputInit(self):
        self.lock = thread.allocate_lock()
        self.responses = []
        self.boundToInput = self.makeListener() 
    def makeListener(self):
        try:
            compReg.getLock().acquire()
            compReg.getComponent(self['SensorNetworkId']).addListener(self)
            compReg.getLock().release()
            return True
        except Exception as ex:
            compReg.getLock().release()
            return False
    
    def sensingLoop(self):
        #TODO: Lock on self.responses
        if not self.boundToInput:
            self.boundToInput = self.makeListener()
        for r in self.responses:
            r['Location'] = (int(r['SensorId'])*self['SensorSpacing'], self['Y'])
        if self.responses:
            self.respond(self.responses)
        self.responses = []
    def processResponse(self, sensorDict, eventDict):
        self.responses += eventDict
