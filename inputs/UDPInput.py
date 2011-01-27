from operationscore.Input import *
import socket
class UDPInput(Input):
    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
    def sensingLoop(self):
        (data,address) = self.sock.recvfrom(1024)
        dataDict = {'data':data, 'address':address}
        self.respond(dataDict)
             
