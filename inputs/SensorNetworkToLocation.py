"""SensorNetworkToLocation converts data from a sensor network in terms of ids into their actual
locations.
Params:
<SensorNetworkId> -- the cid of the component generating raw sensor data -- Note that this component may
need to be below that component in the XML
<SensorSpacing> -- sensors location = int(id)*SensorSpacing 
<Y> -- the Y location specified by the user
<Mode> -- Simulator OR SensorNetwork  -- Set to [Simulator] for taking data from
<InputType> -- Simulator OR SensorNetwork  -- Set to [Simulator] for taking data from
PedestrianSimulator.  Set to SensorNetwork to take data from UDP input.
SensorNetworkToLocation takes packets with field <SensorId>int</SensorId>.  It adds a <Location> tag
to the response which it infers from the SensorId field.

"""

#TODO: add logging
from operationscore.Input import *
import util.ComponentRegistry as compReg
import thread
from logger import main_log
import util.TimeOps as timeOps
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
    def grabBits(self, p):
        return bin(ord(p))[2:].zfill(8) 
    def parseSensorBinaryPacket(self,p, firstBitIndex):
        if len(p) != 5:
            print 'bad length'
        packet = []
        for i,hexByte in enumerate(p):
            bits = grabBits(hexByte)
            for b,j in enumerate(bits):
                if b == 1:
                    sensorId = firstBitIndex + i*8 + j
                    output.append({'SensorId':sensorId, 'Responding':timeOps.time()})
            #send output as necessary 
        return output
    def parseSensorPacket(self, p):
        #sensorid:XXXX#sensorid:XXXX#sensorid:XXXX
        #Packet:
        #10 Bytes
        import pdb; pdb.set_trace()
        packets = p.split('#')
        output = []
        for s in packets:
            if s != '':
                sensorId, packetData = s.split(':')
                for i,val in enumerate(packetData):
                    if val == '1':
                        #print 'responding:',i
                        output.append({'SensorId':int(sensorId)*len(packetData)+i, 'Responding':timeOps.time()})
                        print 'output'
        return output
    def sensingLoop(self):
        #TODO: Lock on self.responses
        if not self.boundToInput:
            self.boundToInput = self.makeListener()
        if self['Mode'] == 'SensorNetwork':
            tempResponses = []
            for r in self.responses:
                startIndex = 0 #TODO: lookup from table
                tempResponses += self.parseBinarySensorPacket(r['data'], startIndex) 

            self.responses = tempResponses

        for r in self.responses:
            if self['Y']:
                r['Location'] = ((int(r['SensorId'])+1)*self['SensorSpacing'], self['Y'])
            else:
                r['Location'] = ((int(r['SensorId'])+1)*self['SensorSpacing'], 20)
        if self.responses:
            self.respond(self.responses)
        self.responses = []

    def processResponse(self, sensorDict, eventDict):
        if(isinstance(eventDict, list)):
            self.responses += eventDict
        else:
            self.responses.append(eventDict)
