from operationscore.Renderer import *
import util.PacketComposition as composer 
import util.NetworkOps as network
import socket,pdb
port = 6038
#Renderer for a Specific Light System.
class IndoorRenderer(Renderer):
    def initRenderer(self):
        self.stripLocations = {} #Dict that stores info necessary to render to
        #strips
        self.sockets = {} #dict of (IP)->Socket
        #a strip
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
        try:
            for pixelStrip in lightSystem.pixelStrips:
                stripId = pixelStrip.argDict['Id']
                (ip, port) = self.stripLocations[stripId] 
                if not ip in self.sockets: #do we have a socket to this
                    #strip? if not, spin off a new one
                    self.sockets[ip] = network.getConnectedSocket(ip,port)
                packet = composer.composePixelStripPacket(pixelStrip, port) 
                self.sockets[ip].send(packet, 0x00)
        except:
            pass #Rendering error.  Log it. LOG

