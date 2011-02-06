from operationscore.Input import *
import socket
class UDPInput(Input):
    """UDPInput is a barebones UDP Input class.  It takes any data it receives and adds it to the
    'data' element of the response dict.  It also notes the 'address'.  Specify:
    <Port> -- the Port to listen on."""

    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Put the socket in UDP mode
        self.sock.bind((HOST, PORT))
    def sensingLoop(self):
        (data,address) = self.sock.recvfrom(1024)
        dataDict = {'Data':data, 'address':address}
        self.respond(dataDict)
             
