import util.Strings as Strings
import pdb
from operationscore.Input import *
import socket, json, time
import logging as main_log
import string
from select import select

class TCPInput(Input):
    """TCPInput is a input to receive input on a TCP port.  In its current incarnation, it parses
    json data into python dicts.  Warning: contains a bug where init will hang until it receives a
    connection.  Specify:
    <Port> -- Port number to listen on."""
    def inputInit(self):
        self.HOST = ''                 # Symbolic name meaning all available interfaces
        self.PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024
        self.IS_RESPONDING = 1
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)

        isreadable=select([self.sock],[],[], 0)[0]
        self.conn = None
        if isreadable:
            (self.conn, self.address) = self.sock.accept()

    def sensingLoop(self):
        if self.conn == None:
            isreadable=select([self.sock],[],[], 0)[0]
            if isreadable:
                (self.conn, self.address) = self.sock.accept()
            else:
                return
        
        data = self.conn.recv(self.BUFFER_SIZE)
        main_log.debug('Incoming data', data)
        
        if not data or 'end' in data: # data end, close socket
            main_log.debug('End in data')
            print 'end of stream'
            self.IS_RESPONDING = 0
            self.conn.close()
            self.sock.close()
        
        if self.IS_RESPONDING == 1: # if 'responding', respond to the received data		       	
            try:
                for datagroup in data.split('\n'):
                    if datagroup != None and datagroup != '':
                        dataDict = json.loads(datagroup)
                        #if dataDict['type'] != 1:
                        #print dataDict
                        self.respond(dataDict)
            except Exception as exp:
                print str(exp) 
        else:
            # if not 'responding', don't respond to data and restart socket
            # * an incomplete hack for now. will be changed if same-type-multi-Input is implemented.

            self.IS_RESPONDING = 1
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.HOST, self.PORT))
            self.sock.listen(1)
            (self.conn, self.address) = self.sock.accept()
