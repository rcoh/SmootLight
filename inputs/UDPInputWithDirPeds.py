from inputs.SynchDirPeds import *
from inputs.SynchSenseNetLoc import *
from operationscore.Input import *
import socket
import json
class UDPInputWithDirPeds(Input):
    """UDPInput is a barebones UDP Input class.  It takes any data it receives and adds it to the
    'data' element of the response dict.  It also notes the 'address'.  Specify:
    <Port> -- the Port to listen on.
    <Mode> -- [Raw] or JSON -- if the mode is set to JSON, packets will be parsed as JSON"""

    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        self.dirPeds = SynchDirPeds({})
        self.sensNetLoc = SynchSenseNetLoc({'SensorSpacing':45, 'Mode':'SensorNetwork'})
    
    def socketLoop(self):
        (data,address) = self.sock.recvfrom(1024)
        while data:
            if not self['Mode'] or self['Mode'] == 'Raw':
                dataDict = {'data':data, 'address':address}
            else:
                dataDict = json.loads(data)
                dataDict['Address'] = address
            pedData = self.processPed(dataDict)
            self.respond(pedData)
            #print 'data'
            (data, address) = self.sock.recvfrom(1024)
    
    def processPed(self, data):
        data = self.sensNetLoc.processInput(data)
        data = self.dirPeds.processInput(data)
        return data
    def run(self):
        self.socketLoop()


