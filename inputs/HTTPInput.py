import web
from operationscore.Input import *
class HTTPInput(Input):
    def behaviorInit(self):
        global responseQueue
        urls = ("lights.json", "Responder")
        class Responder:
            def GET(self):
                global responseQueue 
                params = web.input()
                print params
