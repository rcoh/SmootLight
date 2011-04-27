from operationscore.Renderer import *
import util.PacketComposition as composer 
import util.NetworkOps as network
import util.TimeOps as timeops
import socket,pdb
sock_port = 6038
class IndoorRenderer(Renderer):
    """IndoorRenderer is a renderer for a specific Light System"""

    def initRenderer(self):
        self.stripLocations = {} #Dict that stores info necessary to render to strips
        self.sockets = {} #dict of (IP)->Socket
        #a strip
        powerSupplies = self.argDict['PowerSupply']
        if not type(powerSupplies) == type([]):
            powerSupplies = [powerSupplies]
        for powerSupply in powerSupplies: 
            ip = powerSupply['IP']
            stripsInPowerSupply = powerSupply['PortMapping']
            for stripId in stripsInPowerSupply:
                self.stripLocations[stripId] = (ip, stripsInPowerSupply[stripId])
        self.broadSocket = network.getBroadcastSocket(6038) 
    def render(self, lightSystem, currentTime=timeops.time()): 
        for pixelStrip in lightSystem.strips:
            stripId = str(pixelStrip.argDict['Id'])
            (ip, port) = self.stripLocations[stripId] 
            if not ip in self.sockets: #do we have a socket to this
                self.sockets[ip] = network.getConnectedSocket(ip,sock_port)
            packet = composer.composePixelStripPacket(pixelStrip.values, port)
            try:
                self.sockets[ip].send(packet, 0x00)
            except:
                pass
