import Util, Input
import socket
class UDPInput(Input.Input):
    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        print 'UDPINIT'
    def sensingLoop(self):
            print 'udploop'
            (data,address) = self.sock.recvfrom(1024)
            dataDict = {'data':data, 'address':address}
            print 'LOLOLOLOL'
            self.respond(dataDict)
             
