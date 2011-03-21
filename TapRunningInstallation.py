#!/usr/bin/python

import socket
from select import select
#from xml.etree.ElementTree import ElementTree
import pdb, sys, time, thread
#import util.TimeOps as clock
#import util.Config as configGetter 
#import util.ComponentRegistry as compReg
#import util.BehaviorQuerySystem as bqs
import json

class TapConnection(object):
    """ This class handles connection to server """
    def __init__(self,host,port):
       
        self.host = host
        self.port = port
        

    def sendMsg(self,outData):


        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       # s.bind((self.host, self.port+1))
        
        s.sendto(outData, (self.host, self.port))
        time.sleep(.1)
        
        
        string = ""
        
        #unlikely, but make sure buffer empty
        while select([s],[],[], 0)[0]:
            (inData,addy) = s.recvfrom(1024)
            string = string + inData
           
        return string
        
    def close(self):
        pass

class MenuTree(object):
     """ TapRunning - maintains state for a running LightInstallation 
         commands: 
           a - print all objects
           p - print all behaviors
           (integer) - select number 
           q - go back / quit
           
           e - edit
           c - create
           d - delete
           """
     
     COMMANDS = {'a':'Objects','b':'Behaviors','p':'Behaviors'}
     
     def __init__(self, connection, msg =''):
        self.connection = connection
        self.nextAction = None
        
        
     def executeSelection(self,command):
        
        cl = command.lower()
        if cl.isdigit():
            if self.nextAction != None:
                self.nextAction(int(cl))
            else:
                print "Got #{} but don't know what to do with it. Try 'h'".format(cl)
            return 0
    
        cl = cl[0]
        
        if cl in ["q","x"]:
            return -1
        elif cl in ["a","b", "p"]:
            print "Getting {}, please wait...".format(self.COMMANDS[cl])
            
            resp = self.connection.sendMsg(json.dumps({"OperationType":"Get"+self.COMMANDS[cl]}))  
            try: 
                resp = json.loads(resp)   
            except:       
                print "response? <",resp, ">" 
                return 0
                
            self.componentList = resp
            
            print "Available %s:\n"%self.COMMANDS[cl]
            
            for n in range(len(resp)):
                print "{:4} {:10}".format(n,resp[n])   
                
        elif cl in ["h","?"]: 
            print self.__doc__

        return 0
        
     def showMenu(self):
        pass
     def acceptInput(self):
        pass

class TapRunningInstallation(object):
    """ This is the main class responsible for console IO """
    def __init__(self):
        self.dieNow = False
 
    def mainLoop(self):
        m = MenuTree(TapConnection('localhost',22332))
        while not self.dieNow: 
            m.showMenu()
            m.acceptInput()
            select = raw_input("> ") 
            if m.executeSelection(select) == -1:
                self.dieNow = True               
    
        m.connection.close()

    def handleDie(self, caller):
        self.dieNow = True
            
def main(argv):
        l = TapRunningInstallation()
        l.mainLoop() 
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nTerminated by keyboard.')
