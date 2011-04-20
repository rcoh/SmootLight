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
           
           p - print all renderable behaviors
           b - print all behaviors
           a - print all objects
           (integer) - select number 
           q - go back / quit
           
           e - edit 
           c - create
           d - delete
           """
     
    ObjectTypes = {'p':'Renderables','a':'Objects','b':'Behaviors'}
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
         
        #  should put processing for edit inputs here. if generalized callback exists, try using input  
        # all the following should be special case when input callback = None
        if cl in ["q","x"]:
            return -1
        elif cl in self.ObjectTypes.keys(): 
            self.commandDict['OperationDetail'] = self.ObjectTypes[cl]
            
            self.nextAction = lambda x: self.requestSpecificItem(x)
            
            if len(cs) > 1 and cs[1].isdigit() and self.componentList != None:
                self.requestSpecificItem(int(cs[1]))
            else:
                print "Getting {}, please wait...".format(self.ObjectTypes[cl])
                self.currentObject = None
                
                self.commandDict['OperationArg'] = None
                self.requestItems()
        elif cl in ["e"]:
            
            self.nextAction = lambda x: self.initiateEdit(x)
            
            if len(cs) > 1 and cs[1].isdigit():
                # if digit known, call command to get details of object first,  invisible mode
                if self.requestSpecificItem(int(cs[1]), True) < 0:
                    return
                #print "do some prompting to figure out what needs to be changed"
 
            self.initiateEdit()

        elif cl in ["h","?"]: 
            print self.__doc__
            self.nextAction = None
        elif cl in ["c","d"]:
            print "unimplemented"
            self.nextAction = None
        else: 
            if cl != "":
                print "syntax error, use 'h' for help"

        return 0
        
    def showMenu(self):
        pass
    def acceptInput(self):
        pass
        
    def requestSpecificItem(self,index, is_quiet=False):
        if self.componentList == None:
            print "Specify whether you're talking about renderables (p) objects (a) or all behaviors (b)."
            return -1
        elif len(self.componentList)-1 < index:
            print "No element with index {}.".format(index)
            self.commandDict['OperationArg'] = None
            self.nextAction = None
            return -1
        else:
            if not is_quiet:
                print "Retrieving specific {}...\n".format(self.commandDict['OperationDetail'][:-1])
            self.commandDict['OperationArg'] = self.componentList[index][0] 
            self.requestItems(is_quiet)
            return 0
        
         
    def requestItems(self, is_quiet=False):
        self.commandDict['OperationType'] = 'Read'
       # self.commandDict['OperationDetail'] = command
        
        #if not(is_quiet):
        #    print self.commandDict
        
        resp = self.connection.sendMsg(json.dumps(self.commandDict))  
        if resp == "":
            print "No (timely) response. Is server running? Is SystemConfigMutator Behavior and tap input in the configuration?"
            return 0
        try: 
            resp = json.loads(resp)   
        except:       
            print "couldn't parse response- not json? <",resp, ">" 
            return 0
        
        if self.commandDict['OperationArg']  == None:
            
            self.componentList = resp
            
            self.printComponentList()
            
        else:
            self.currentObject = resp
            self.printCurrentObject(is_quiet)
            
    def printComponentList(self):
        print "Available %s:\n"%self.commandDict['OperationDetail']
        resp = self.componentList
        for n in range(len(resp)):
            if len(resp[n]) > 1:
                print "{:4}  {:15} {:5}".format(n,resp[n][0], resp[n][1] and 'True' or 'False') 
            else:
                print "{:4}  {:10}".format(n,resp[n][0])
                
    def printCurrentObject(self,is_quiet):
        if not(is_quiet):
            for r in re.split(''',(?=(?:[^\[\]]|\[[^\[]*\])*$)''', self.currentObject[1:-1]): #   resp.split(','):
                if r.find('parentScope') == -1:
                    print " "+r.replace("'","").strip()
            
    def initiateEdit(self, index=None):
         #pdb.set_trace()
         #print self.commandDict,"\n\n",index
         if self.currentObject == None or self.commandDict['OperationArg'] == None:
             print "Need to specify which object."
             return 0
         elif self.currentObject.find('RenderToScreen') == -1:
             print "Object not renderable."
             return 0
         else:             
            if index != None:
                if self.requestSpecificItem(index,False) < 0:
                    return 
            else:
                self.printCurrentObject(False)
         
            co=self.currentObject[1:-1]#.rstrip('}').lstrip('{')
                            
            # split on commas unless inside square brackets
            co = re.split(''',(?=(?:[^\[\]]|\[[^\[]*\])*$)''', co)
            
            
            currentRender = [map(unicode.strip,i.replace("'","").split(':')) for i in co if i.find('RenderToScreen') != -1][0]
            #pdb.set_trace()
            print self.commandDict['OperationArg']+"'s "+str(currentRender[0])+" is "+str(currentRender[1])+" -- ",
            
            if currentRender[1][0].lower() == 'f':
                value = False
                confirm = raw_input("activate (y/N)? ")
            else:
                value = True
                confirm = raw_input("deactivate (y/N)? ")
                
            if confirm != "" and confirm[0] == 'y':
                value = not value
                
            self.commandDict['OperationType'] = 'Update'
            self.commandDict['ComponentId'] = filter(lambda x: x.find('Id')!=-1,co)[0].split(":")[1].strip(" '")
            self.commandDict['Value'] = value
            self.commandDict['ParamName'] = "RenderToScreen"#selection[0].strip("'")
            resp = self.connection.sendMsg(json.dumps(self.commandDict))
            
            self.commandDict = {'OperationArg':self.commandDict['OperationArg'],
                                'OperationDetail':self.commandDict['OperationDetail']}
            # co = [i for i in co if i.find(': <') == -1]
            # for n in range(len(co)):
            #     print n, ": ", co[n].strip()
            #             
            # print "edit what?"    
            # i = raw_input("> ")
            # 
            # #argDict=eval('{%s}'%','.join(co))                
            # if i.isdigit() and int(i) < len(co):
            #     selection = map(unicode.strip,co[int(i)].split(':'))
            #     value = raw_input("set "+ selection[0]+ " to: " )
            #     
            #     print "setting ", selection[0]," to '",value,"'"      
            #     self.commandDict['OperationType'] = 'Update'
            #     self.commandDict['ComponentId'] = filter(lambda x: x.find('Id')!=-1,co)[0].split(":")[1].strip(" '")
            #     self.commandDict['Value'] = value
            #     self.commandDict['ParamName'] = selection[0].strip("'")
            #     resp = self.connection.sendMsg(json.dumps(self.commandDict)) 
            #     print resp
            #     self.commandDict = {'OperationArg':None}
            #
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
