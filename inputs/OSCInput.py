from operationscore.Input import *
import liblo
from logger import main_log


class OSCInput(Input):
    def inputInit(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = self['Port']              # Arbitrary non-privileged port
	self.server = liblo.Server(PORT)
	self.server.add_method(None,None, self.fallback)
#	except liblo.ServerError, err:
 #   		main_log.error(str(err))

    def fallback(self,path,args,types, src):
            self.respond({'Path':path,'Type':types[0],'Value':args[0]})
    def sensingLoop(self):
            self.server.recv(100)
            pass#(data,address) = self.sock.recvfrom(1024)
            #dataDict = {'data':data, 'address':address}
            #self.respond(dataDict)
             
