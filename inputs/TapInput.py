# import util.Strings as Strings
import pdb
from operationscore.Input import *
import socket, json, time
# import logging as main_log
# import string
# from select import select
from time import sleep
class TapInput(Input):
    """TapInput is a hacked input to perform TCP i/o for remote control.  Specify:
    <Port> -- Port to listen on."""
    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self.argDict['Port']              # Arbitrary non-privileged port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        #self.sock.settimeout(1)

    def sensingLoop(self):
        try: 
            (data,address) = self.sock.recvfrom(1024)
            
        except Exception as e:
            print "exception in TapInput",str(e)
            return
        
        def reply(msg):
            self.sock.sendto(msg,address)

        dataDict = json.loads(str(data))
        dataDict['Callback'] = reply
        
        self.respond(dataDict)
        
        # self.sock.sendto('', (host, port))
          #       
          # try:
          #     for datagroup in data.split('\n'):
          #         if datagroup != None and datagroup != '':
          #             dataDict = json.loads(datagroup)
          #             #if dataDict['type'] != 1:
          #             #print dataDict
          #             self.respond(dataDict)
          # except Exception as exp:
          #     print str(exp)
