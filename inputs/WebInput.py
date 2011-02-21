import web, sys, threading, json, webbrowser
from operationscore.Input import *
import util.ComponentRegistry as compReg

queue = []
queueLock = threading.Lock()

class WebInput(Input):
    """Start a webserver, serving static files for the web interface and
        processing input in the form of HTTP GET requests.  Inputs consist
        of an array of (action, parameter) pairs, with action being derived
        from the URL requested, which is of the form /input/{action}, while
        parameters are given in a dictionary derrived from the URL parameters.
        
        URLs not prefixed with /input/ will interpreted as requests for static
        content and served (after a redirect) from the /static directory of the
        top-level project folder.
    """
    
    def inputInit(self):
        self.hostname = self.argDict['Hostname']
        self.port = int(self.argDict['Port'])
        compReg.registerComponent(self, 'Webserver')
        
        urls = ('/(.*)', 'WebHandler')
        env = globals()
        env['sys'].argv = []
        app = web.application(urls, env)
        
        self.server_thread = threading.Thread(target=app.run)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        webbrowser.open('http://'+self.hostname+':'+str(self.port))
    
    def getPort(self):
        return self.port
    
    def sensingLoop(self):
        queueLock.acquire()
        inputs = []
        while len(queue) > 0:
            inputs.append(queue.pop())
        resp = dict(inputs=inputs)
        queueLock.release()
        self.respond(resp)

class WebHandler(object):
    def GET(self, action):
        
        if action == '':
            action = 'index.html'
        
        if not action.startswith('input/'):
            raise web.Found('/static/'+action)
        
        params = web.input()
        queueLock.acquire()
        queue.append((action, params))
        queueLock.release()
        
        return json.dumps(dict(success=True))
