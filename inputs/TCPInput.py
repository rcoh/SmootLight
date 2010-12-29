import util.Strings as Strings
from operationscore.Input import *
import socket, json, time
import logging as main_log
class TCPInput(Input):
    def inputInit(self):
        self.HOST = ''                 # Symbolic name meaning all available interfaces
        self.PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024
        self.IS_RESPONDING = 1
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
        (self.conn, self.address) = self.sock.accept()

    def sensingLoop(self):
        data = self.conn.recv(self.BUFFER_SIZE)
        main_log.debug('Incoming data', data)
        if not data or 'end' in data: # data end, close socket
            main_log.debug('End in data')
            self.IS_RESPONDING = 0
            self.sock.close()
        
        if self.IS_RESPONDING == 1: # if 'responding', respond to the received data			
            dataDict = json.loads(data)
            # socketDict = {'data':dataDict, 'address':self.address}
            socketDict = {Strings.LOCATION: (100 * (1 - dataDict['x'] / 10), 25 * (1 + dataDict['y'] / 10))} # like PygameInput
            
            self.respond(socketDict)
        else:
            # if not 'responding', don't respond to data and restart socket
            # * an incomplete hack for now. will be changed if same-type-multi-Input is implemented.
            time.sleep(1)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.HOST, self.PORT))
            self.sock.listen(1)
            (self.conn, self.address) = self.sock.accept()
            self.IS_RESPONDING = 1
             
