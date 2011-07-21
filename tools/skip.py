#!usr/bin/python

import socket
from select import select
import sys, time
import json, re

ADDY = 'localhost'
#ADDY = '10.32.2.1'




SKIP_JSON='{"OperationArg": "bodysequence", "OperationDetail": "Renderables", "Value": true, "OperationType": "Update", "ParamName": "command_skip()", "ComponentId": "bodysequence"}'


class TapConnection(object):
    """ This class handles connection to server """
    def __init__(self,host,port):
       
        self.host = host
        self.port = port
        

    def sendMsg(self,outData, maxretry = 5, interval = 1):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.bind((self.host, self.port+1))

        # make sure buffer empty
        while select([s],[],[], 0)[0]:
                (inData,addy) = s.recvfrom(1024)

        s.sendto(outData, (self.host, self.port))
        time.sleep(.1)
        #s.sendto(outData, (self.host, self.port))

        string = ""

        while string == "" and maxretry > 0:
            maxretry -= 1

            # on last attempt resend the message ? need to protect against json errors
            #if maxretry == 0:
            #    interval *= 3
            #    s.sendto(outData, (self.host, self.port))

            time.sleep(interval)
            while select([s],[],[], 0)[0]:
                    (inData,addy) = s.recvfrom(2048)
                    string = string + inData
         #if string == "":
         #    return ""
         #return "["+string.split('][')[-1].strip('[]')+']'

        return string


        
    def close(self):
        pass

class TapRunningInstallation(object):
    """ This is the main class responsible for console IO """
    def __init__(self):
        self.dieNow = False
 
    def skip(self, n):
        c=TapConnection(ADDY,22332)
        for i in range(n):
            c.sendMsg(SKIP_JSON)
            print "Skipping.. "+str(i)
        
        self.dieNow = True
        c.close()
    
        c.close()

    def handleDie(self, caller):
        self.dieNow = True
            
def main(argv):
        if len(argv) > 1 and argv[1].isdigit():
            nskip = int(argv[1])
        else:
            nskip = 1

        l = TapRunningInstallation()
        l.skip(nskip)
 
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nTerminated by keyboard.')
