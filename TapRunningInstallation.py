#!/usr/bin/python

import socket
from select import select
#from xml.etree.ElementTree import ElementTree
import pdb, sys, time, thread
#import util.TimeOps as clock
#import util.Config as configGetter 
#import util.ComponentRegistry as compReg
#import util.BehaviorQuerySystem as bqs
import json, re

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
                    (inData,addy) = s.recvfrom(1024)
                    string = string + inData
        #if string == "":
        #    return ""
        #return "["+string.split('][')[-1].strip('[]')+']'
        
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
        self.lastAction = None
        
    def executeSelection(self,command):
#        self.commandDict['CurrentCommand'] = command
        
        cl = command.strip().lower()
        if cl.isdigit():
            if self.nextAction != None:
                self.nextAction(int(cl))
            else:
                print "Got #{0} but don't know what to do with it. Try 'h'".format(cl)
            return 0
            
    
        cs = cl.split(' ')
        cl = cs[0]
         
        if cl in ["q","x"]:
            return -1
        elif cl in ["a","b", "p"]:
            self.nextAction = lambda x: self.sendCommandInt(cl,x)
            print "Getting {0}, please wait...".format(self.COMMANDS[cl])
            self.lastAction = self.COMMANDS[cl]
            if len(cs) > 1 and cs[1].isdigit() and self.componentList != None:
                self.sendCommandInt(self.lastAction,int(cs[1]))
            else:
                self.currentObject = None
                
                self.commandDict['OperationArg'] = None
                self.sendCommand(self.lastAction)
        elif cl in ["e"]:
            if len(cs) > 1 and cs[1].isdigit():
                # if digit known, call command to get details of object first,  invisible mode
                self.sendCommandInt(self.lastAction, int(cs[1]), True)
                #print "do some prompting to figure out what needs to be changed"
            if 1:
                
                if self.currentObject == None:
                    print "Need to specify which object."
                    return
               #pdb.set_trace()
                co=self.currentObject[1:-1]#.rstrip('}').lstrip('{')
                
                # split on commas unless inside square brackets
                co = re.split(''',(?=(?:[^\[\]]|\[[^\[]*\])*$)''', co)
                
                
                co = [i for i in co if i.find(': <') == -1]
                for n in range(len(co)):
                    print n, ": ", co[n].strip()
            
                print "edit what?"    
                i = raw_input("> ")
                
                #argDict=eval('{%s}'%','.join(co))                
                if i.isdigit() and int(i) < len(co):
                    selection = map(unicode.strip,co[int(i)].split(':'))
                    value = raw_input("set "+ selection[0]+ " to: " )
                    
                    print "setting ", selection[0]," to '",value,"'"      
                    self.commandDict['OperationType'] = 'Update'
                    self.commandDict['ComponentId'] = filter(lambda x: x.find('Id')!=-1,co)[0].split(":")[1].strip(" '")
                    self.commandDict['Value'] = value
                    self.commandDict['ParamName'] = selection[0].strip("'")
                    resp = self.connection.sendMsg(json.dumps(self.commandDict)) 
                    print resp
                    self.commandDict = {'OperationArg':None}
                    
                
        elif cl in ["h","?"]: 
            print self.__doc__
            self.nextAction = None
            self.lastAction = None
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
        
    def sendCommandInt(self,command,index, is_quiet=False):
        if self.componentList == None:
            print "Specify whether you're talking about all objects or just behaviors (a/b)."
        elif len(self.componentList)-1 < index:
            print "No element with that index."
        else:
            self.commandDict['OperationArg'] = self.componentList[index] 
            self.sendCommand(command, is_quiet)
        
         
    def sendCommand(self, command, is_quiet=False):
        self.commandDict['OperationType'] = 'Read'
        self.commandDict['OperationDetail'] = command
        
        #if not(is_quiet):
        #    print self.commandDict
        
        resp = self.connection.sendMsg(json.dumps(self.commandDict))  
        if resp == "":
            print "Operation timeout. Is server running? Are SystemConfigMutator behavior and tap input in the configuration?"
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
                print "{0:4} {1:10}".format(n,resp[n])   
        else:
            self.currentObject = resp
            if not(is_quiet):
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

