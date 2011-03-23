from operationscore.Input import *
from json

class FixedInput(Input):
    """
    FixedInput takes a static JSON formatted data in the config file, and calls repond on it in every loop.
    """
    def inputInit(self):
        self.inputContent = json.loads(self.argDict['Content'])

    def sensingLoop(self):
        self.respond(inputContent)
