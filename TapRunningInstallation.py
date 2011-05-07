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
<<<<<<< HEAD
        
        #unlikely, but make sure buffer empty
        while select([s],[],[], 0)[0]:
            (inData,addy) = s.recvfrom(1024)
            string = string + inData
           
=======

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

>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
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
<<<<<<< HEAD
        self.lastAction = None
=======
        self.lastcl = ""
        self.lastindex = None
>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
        
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
<<<<<<< HEAD
        elif cl in ["a","b", "p"]:
            self.nextAction = lambda x: self.sendCommandInt(cl,x)
#            print "Getting {}, please wait...".format(self.COMMANDS[cl])
            self.lastAction = self.COMMANDS[cl]
            if len(cs) > 1 and cs[1].isdigit() and self.componentList != None:
                self.sendCommandInt(self.lastAction,int(cs[1]))
=======
        elif cl in self.ObjectTypes.keys(): 
            self.lastindex = None
            if self.lastcl != cl:
                self.componentList = None
                
            self.lastcl = cl
            
            self.commandDict['OperationDetail'] = self.ObjectTypes[cl]
            
            self.nextAction = lambda x: self.requestSpecificItem(x)
            
            if len(cs) > 1 and cs[1].isdigit() and self.componentList != None:              
                self.requestSpecificItem(int(cs[1]))                
>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
            else:
                self.currentObject = None
                
                self.commandDict['OperationArg'] = None
<<<<<<< HEAD
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
                    
                
=======
                self.requestItems()
        elif cl in ["e","t"]:
            
            self.nextAction = lambda x: self.initiateEdit(x)
            idx = None
            if len(cs) > 1 and cs[1].isdigit():
                # if digit known, call command to get details of object first,  invisible mode
                #if self.requestSpecificItem(int(cs[1]), True) < 0:
                #    return
                idx=int(cs[1])
                    
                #print "do some prompting to figure out what needs to be changed"
 
            self.initiateEdit(idx,(cl[0] == "t"))

>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
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
<<<<<<< HEAD
            self.commandDict['OperationArg'] = self.componentList[index] 
            self.sendCommand(command, is_quiet)
=======
            if not is_quiet:
                print "Retrieving specific {0}...\n".format(self.commandDict['OperationDetail'][:-1])
            self.commandDict['OperationArg'] = self.componentList[index][0] 
            self.requestItems(is_quiet)
            self.lastindex = index
            return 0
>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
        
         
    def sendCommand(self, command, is_quiet=False):
        self.commandDict['OperationType'] = 'Read'
        self.commandDict['OperationDetail'] = command
        
        if not(is_quiet):
            print self.commandDict
        
        resp = self.connection.sendMsg(json.dumps(self.commandDict))  
        if resp == "":
            print "No response. Is server running? Is SystemConfigMutator Behavior and tap input in the configuration?"
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
<<<<<<< HEAD
            if not(is_quiet):
                for r in resp.split(','):
                    print r
            
=======
            self.printCurrentObject(is_quiet)
            
    def printComponentList(self):
        print "Available %s:\n"%self.commandDict['OperationDetail']
        resp = self.componentList
        for n in range(len(resp)):
            if len(resp[n]) > 1:
                print "{0:4}  {1:15} {2:5}".format(n,resp[n][0], resp[n][1] and 'True' or 'False') 
            else:
                print "{0:4}  {1:10}".format(n,resp[n][0])
                
    def printCurrentObject(self,is_quiet):
        if not(is_quiet):
            for k,v in self.currentObject.items():#re.split(''',(?=(?:[^\[\]]|\[[^\[]*\])*$)''', self.currentObject[1:-1]): #   resp.split(','):
                if k != 'parentScope':
                    print k,":",v
            
    def initiateEdit(self, index=None, is_toggle = False):
         #pdb.set_trace()
         #print self.commandDict,"\n\n",index
         if index == None and (self.currentObject == None or self.commandDict['OperationArg'] == None):
             print "Need to specify which object."
             return 0
         #elif self.currentObject.find('RenderToScreen') == -1:
         #    print "Object not renderable."
         #    return 0
         else:             
            if index != None:
                if self.requestSpecificItem(index,False) < 0:
                    return
            elif self.requestSpecificItem(self.lastindex,True) < 0:
                    return
            
            #else:
            #    self.printCurrentObject(False)
         
            #co=self.currentObject[1:-1]#.rstrip('}').lstrip('{')
                            
            # split on commas unless inside square brackets
            #co = re.split(''',(?=(?:[^\[\]]|\[[^\[]*\])*$)''', co)
            #co = re.split(''',(?=(?:[^{}]|\[[^{}]*})*$)''', co)
            
            if is_toggle:
                
                if not self.currentObject.has_key('RenderToScreen'):
                    print "Object not renderable."
                    return 0
            
                currentRender = self.currentObject['RenderToScreen']
                #pdb.set_trace()
                print self.commandDict['OperationArg']+"'s RenderToScreen is "+str(currentRender)+" -- ",
            
                if not currentRender:
                    value = False
                    confirm = raw_input("activate (y/N)? ")
                else:
                    value = True
                    confirm = raw_input("deactivate (y/N)? ")
                
                if confirm != "" and confirm[0] == 'y':
                    value = not value
                
                self.commandDict['OperationType'] = 'Update'
                self.commandDict['ComponentId'] = self.currentObject['Id'] #filter(lambda x: x.find('Id')!=-1,co)[0].split(":")[1].strip(" '")
                self.commandDict['Value'] = value
                self.commandDict['ParamName'] = "RenderToScreen"#selection[0].strip("'")
                resp = self.connection.sendMsg(json.dumps(self.commandDict))
            else:
                
                if not self.currentObject.has_key('Mutable'):
                    print "Object not mutable."
                    return 0
                    
                print self.commandDict['OperationArg']+"'s API: "
                n = -1
                mkeys= self.currentObject['Mutable'].keys()
                functions = []
                for m in mkeys:
                    n+=1
                    if not self.currentObject.has_key(m):
                        print "{0:4}  {1:12}()".format(n,m)
                        functions.append(m)
                    else:
                        print "{0:4}  {1:12} {2}".format(n,m,self.currentObject[m])
                
                print "edit what?"    
                i = raw_input("> ")
                
                if i.isdigit() and int(i) < (len(mkeys)):
                    selection = mkeys[int(i)]#map(unicode.strip,co[int(i)].split(':'))
                    
                    if selection in functions:
                        value = raw_input("call function "+selection+ "()? (y/N)" )
                        if len(value)>0 and value[0].lower() == 'y':
                                value = True
                                print "calling "+selection+"() "          
                        else:
                                value = False
                        

                    else:
                        value = raw_input("set"+ selection+ "to: " )
                        print "setting ", selection," to '",value,"'"    
                      
                    self.commandDict['OperationType'] = 'Update'
                    self.commandDict['ComponentId'] = self.currentObject['Id']#filter(lambda x: x.find('Id')!=-1,co)[0].split(":")[1].strip(" '")
                    self.commandDict['Value'] = value
                    self.commandDict['ParamName'] = selection.strip("'")
                    resp = self.connection.sendMsg(json.dumps(self.commandDict)) 
                    print resp
                else:
                    if i =="":
                        print "cancelled"
                    elif not i.isdigit():
                        print "syntax error"
                    else:
                        print "index out of range"
            
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
>>>>>>> 1db044965cb06fdfea4304bcc80a1dc575b202cd
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

