from xml.etree.ElementTree import ElementTree
from pixelcore.Screen import * 
from pixelcore.PixelStrip import *
import pdb, sys, time, Util
from pygame.locals import *
#Python class to instantiate and drive a Screen through different patterns,
#and effects.
class LightInstallation:
    def __init__(self, configFileName):
        self.inputs = {} #dict of inputs and their bound behaviors, keyed by InputId
        self.behaviors = {}
        self.screen = Screen()
        config = Util.loadConfigFile(configFileName)
        rendererConfig = config.find('RendererConfiguration')
        layoutConfig = config.find('LayoutConfiguration')
        inputConfig = config.find('InputConfiguration')
        behaviorConfig = config.find('BehaviorConfiguration')
        self.initializeLights(layoutConfig)
        self.initializeRenderers(rendererConfig)
        self.initializeInputs(inputConfig)
        self.initializeBehaviors(behaviorConfig)
        
        self.mainLoop()
    def initializeLights(self, layoutConfig):
        layoutEngines = self.initializeComponent(layoutConfig)
        [self.addPixelStrip(l) for l in layoutEngines]
    def addPixelStrip(self, layoutEngine):
        pixelStrip = PixelStrip(layoutEngine)
        self.screen.addStrip(pixelStrip)
    def initializeInputs(self, inputConfig):
        inputs = self.initializeComponent(inputConfig)
        for inputClass in inputs:
            inputClass.start()
            self.inputs[inputClass.argDict['InputId']] = (inputClass, [])
    def initializeRenderers(self, rendererConfig):
        self.renderers = self.initializeComponent(rendererConfig) 
        print self.renderers
    def initializeComponent(self, config):
        components = []
        if config != None:
            for configItem in config.getchildren():
                [module,className] = configItem.find('Class').text.split('.')
                exec('from ' + module+'.'+className + ' import *')
                args = Util.generateArgDict(configItem.find('Args'))
                args['parentScope'] = self
                components.append(eval(className+'(args)')) #TODO: doesn't error
                #right
        return components
    def alive(self):
        return True
    def mainLoop(self):
        #self.screen.allOn()
        while 1:
            time.sleep(.1)
            responses = []
            for behaviorId in self.behaviors:
                [responses.append(b) for b in \
                    self.behaviors[behaviorId].timeStep()] #processes all queued inputs
            [self.screen.respond(response) for response in responses if
                    response != []]
            self.screen.timeStep()
            if responses != []:
                print responses
            [r.render(self.screen) for r in self.renderers]
    def initializeBehaviors(self, behaviorConfig):
        behaviors = self.initializeComponent(behaviorConfig)
        for behavior in behaviors:
            print behavior.argDict
            self.addBehavior(behavior)
        print self.inputs
        print self.behaviors
    def addBehavior(self, behavior):
        self.behaviors[behavior.argDict['behaviorId']] = behavior
        for inputId in behavior.argDict['Inputs']:
            self.inputs[inputId][1].append(behavior.argDict['behaviorId'])
    def processResponse(self,inputDict, responseDict):
        #pdb.set_trace()
        inputId = inputDict['InputId']
        boundBehaviors = self.inputs[inputId][1]
        [self.behaviors[b].addInput(responseDict) for b in boundBehaviors]

def main(argv):
    print argv
    if len(argv) == 1:
        l = LightInstallation('LightInstallationConfig.xml')
    else:
        l = LightInstallation(argv[1])
if __name__ == "__main__":
    main(sys.argv)

