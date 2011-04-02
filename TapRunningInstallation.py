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
    commandDict = {'OperationArg':None}
    componentList = None
     
    def __init__(self, connection, msg =''):
        self.connection = connection
        self.nextAction = None
        self.currentObject = None
        
        
    def executeSelection(self,command):
#        self.commandDict['CurrentCommand'] = command
        
        cl = command.strip().lower()
        if cl.isdigit():
            if self.nextAction != None:
                self.nextAction(int(cl))
            else:
                print "Got #{} but don't know what to do with it. Try 'h'".format(cl)
            return 0
            
    
        cs = cl.split(' ')
        cl = cs[0]
         
        if cl in ["q","x"]:
            return -1
        elif cl in ["a","b", "p"]:
            self.nextAction = lambda x: self.sendCommandInt(cl,x)
            print "Getting {}, please wait...".format(self.COMMANDS[cl])
            
            if len(cs) > 1 and cs[1].isdigit() and self.componentList != None:
                self.sendCommandInt(self.COMMANDS[cl],int(cs[1]))
            else:
                self.commandDict['OperationArg'] = None
                self.sendCommand(self.COMMANDS[cl])
        elif cl in ["e"]:
            if len(cs) > 1 and cs[1].isdigit():
                print "do some prompting to figure out what needs to be changed"
            else:
                
                print "edit what?"
                if self.currentObject == None:
                    return
                co=self.currentObject.replace('}','').replace('{','').split(',')
                co = [i for i in co if i.find(': <') == -1]
                for n in range(len(co)):
                    print n, ": ", co[n].strip()
                    
                i = raw_input("> ")
                #argDict=eval('{%s}'%','.join(co))
                if i.isdigit() and int(i) < len(co):
                    selection = map(unicode.strip,co[int(i)].split(':'))
                    value = raw_input("set "+ selection[0]+ " to: >" )
                    print "setting ", selection[0]," to '",value,"'"                
                
        elif cl in ["h","?"]: 
            print self.__doc__
            self.nextAction = None
        elif cl in ["c","d"]:
            print "unimplemented"
        else:
            if cl != "":
                print "syntax error, use 'h' for help"

        return 0
        
    def showMenu(self):
        pass
    def acceptInput(self):
        pass
        
    def sendCommandInt(self,command,index):
        if len(self.componentList)-1 < index:
            print "No element with that index."
        else:
            self.commandDict['OperationArg'] = self.componentList[index] 
            self.sendCommand(command)
        
         
    def sendCommand(self, command):
        self.commandDict['OperationType'] = 'Read'
        self.commandDict['OperationDetail'] = command
        
        print self.commandDict
        
        resp = self.connection.sendMsg(json.dumps(self.commandDict))  
        if resp == "":
            print "No response. Is server running?"
            return 0
        try: 
            resp = json.loads(resp)   
        except:       
            print "couldn't parse response- not json? <",resp, ">" 
            return 0
        
        if self.commandDict['OperationArg']  == None:
            
            self.componentList = resp
            
            print "Available %s:\n"%command
            
            for n in range(len(resp)):
                print "{:4} {:10}".format(n,resp[n])   
        else:
            self.currentObject = resp
            for r in resp.split(','):
                print r
            
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
