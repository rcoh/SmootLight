from Renderer import Renderer
import socket, Util
import pdb
kinetPort = 6038
class IndoorRenderer(Renderer):
    def initRenderer(self):
        #pdb.set_trace()
        self.stripLocations = {} #Dict that stores info necessary to render to
        #strips
        self.sockets = {} #dict of (IP,port)->Socket
        #a strip
#     g   self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        powerSupplies = self.argDict['PowerSupply']
        if not type(powerSupplies) == type([]):
            powerSupplies = [powerSupplies]
        for powerSupply in powerSupplies: 
            ip = powerSupply['IP']
            stripsInPowerSupply = powerSupply['PortMapping']
            for stripId in stripsInPowerSupply:
                self.stripLocations[stripId] = (ip, \
                        stripsInPowerSupply[stripId])
    def render(self, lightSystem): 
        for pixelStrip in lightSystem.pixelStrips:
            stripId = pixelStrip.argDict['Id']
            (ip, port) = self.stripLocations[stripId] 
            if not ip in self.sockets: #do we have a socket to this
                #strip? if not, spin off a new one
                self.sockets[ip] = Util.getConnectedSocket(ip,kinetPort)
            packet = Util.composePixelStripPacket(pixelStrip, port) 
            self.sockets[ip].send(packet, 0x00)

