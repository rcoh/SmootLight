
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
<IPIndexTable> -- Python Dictionary of String->Int representing the first ip address from an arduino
at that address.
SensorNetworkToLocation takes packets with field <SensorId>int</SensorId>.  It adds a <Location> tag
to the response which it infers from the SensorId field.

"""

#TODO: add logging
import util.ComponentRegistry as compReg
from logger import main_log
import util.TimeOps as timeOps
from operationscore.SmootCoreObject import *
class SynchSenseNetLoc(SmootCoreObject):
    def grabBits(self, p):
        return bin(ord(p))[2:].zfill(8) 
    def parseBinarySensorPacket(self,p, firstBitIndex):
        #print 'starting to parse'
        if len(p) != 5:
            print 'bad length'
        packet = []
        for i,hexByte in enumerate(p):
            bits = self.grabBits(hexByte)
            packet += bits
        output = []
        #print packet
        packet = map(int, packet)
        #print packet
        #print sum(packet)
	#import pdb; pdb.set_trace()
        for j,b in enumerate(packet):
            if b == 1:
                #sensorId = firstBitIndex + i*8 + j
                output.append({'SensorId':j, 'Responding':timeOps.time()})
                #print 'responding', j 
            #send output as necessary
        #print 'done parsing'
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
                        #print 'output'
        return output
    def getIndex(self, address):
        ip, port = address
        if self['IPIndexTable']:
            return self['IPIndexTable'][ip]
        else:
            return 0
    def processInput(self, inp):
        #TODO: Lock on self.responses
        if not isinstance(inp, list):
            self.responses = [inp]
        else:
            self.responses = inp
        if self['Mode'] == 'SensorNetwork':
            tempResponses = []
            for r in self.responses:
                startIndex = self.getIndex(r['address']) 
                tempResponses += self.parseBinarySensorPacket(r['data'], startIndex) 

            self.responses = tempResponses

        for r in self.responses:
            if self['Y']:
                r['Location'] = ((int(r['SensorId'])+1)*self['SensorSpacing'], self['Y'])
            else:
                r['Location'] = ((int(r['SensorId'])+1)*self['SensorSpacing'], 20)
		#print r['Location']
        retResps = list(self.responses)
        return retResps
