import SocketServer
from operationscore.Input import *

"""
A rough sketch about how a TCP socket server receives data from the phone (or other stuff).
Some corrections are probably needed from Russell.
Looks good to me -- not really the way I envisioned it, but since the server
we're using has a built in loop.  When we call the reponse method to pass the
data up the pipe, we should use the sensingLoop so that everything stays
thread-safe.
"""
class TCPInput(Input.Input):
	class InputTCPHandler(SocketServer.BaseRequestHandler):
		def handle(self):
			# get data from the TCP socket connected to the client
			self.data = self.request.recv(1024).strip()
			
			pydict = json.loads(self.data) # decode and add to queue 
                        self.responseQueue.append(pydict) 

			"""
			do something to the dict
			"""
			
			self.request.send("yes") # send back confirmation.
	
	def inputInit(self):
		# initialize
		self.host = "localhost"
		self.port = 9999
                self.responseQueue = []
		# start server
		self.server = SocketServer.TCPServer((self.host, self.port), InputTCPHandler)
                self.server.responseQueue = self.responseQueue
		self.server.serve_forever() # server keeps running till Ctrl+C or self.server.shutdown() is called.
			
	def sensingLoop(self):
		# loop action handled through TCPHandler?
		# if check says to shut down the server, shut it.
		if self.doShutDown():
			self.server.shutdown()	
                else:
                    for event in self.responseQueue:
                        self.respond(event)
                    self.responseQueue = []
	  
	def doShutDown(self):
		# do some checks to see if server should be shut down
		return False;
