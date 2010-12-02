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
        self.behaviorOutputs = {} #key: [list of output destinations]
        self.behaviorInputs = {}
        self.componentDict = {}
        self.inputBehaviorRegistry = {} #inputid -> behaviors listening to that
        #input
        #give Util a pointer to our componentRegistry and screen so that everyone can use
        #it
        Util.setComponentDict(self.componentDict)
        self.screen = Screen()
        Util.setScreen(self.screen)
        config = Util.loadConfigFile(configFileName)
        #read configs from xml
        rendererConfig = config.find('RendererConfiguration')
        pixelConfig = config.find('PixelConfiguration')
        inputConfig = config.find('InputConfiguration')
        behaviorConfig = config.find('BehaviorConfiguration')
        mapperConfig = config.find('PixelMapperConfiguration')
        #inits
        self.initializeScreen(pixelConfig)
        self.initializeRenderers(rendererConfig)
        self.initializeInputs(inputConfig)
        self.initializeBehaviors(behaviorConfig)
        self.initializeMapper(mapperConfig)

        self.screen.setMapper(self.mapper)
        #registration in dict
        self.registerComponents(self.renderers)
        self.registerComponents(self.inputs)
        self.registerComponents(self.behaviors)
        #Done initializing.  Lets start this thing!
        self.mainLoop()
    def initializeMapper(self, mapperConfig):
        self.mapper = self.initializeComponent(mapperConfig)[0] #TODO: support
        #multiple mappers
    def initializeScreen(self, layoutConfig):
        pixelAssemblers = self.initializeComponent(layoutConfig)
        [self.addPixelStrip(l) for l in pixelAssemblers]
    def addPixelStrip(self, layoutEngine):
        pixelStrip = PixelStrip(layoutEngine)
        self.screen.addStrip(pixelStrip)
    def initializeInputs(self, inputConfig):
        inputs = self.initializeComponent(inputConfig)
        self.inputs = inputs
        for inputClass in inputs:
            inputClass.start()
            self.inputBehaviorRegistry[inputClass['Id']] = []
            #empty list is list of bound behaviors
    def initializeRenderers(self, rendererConfig):
        self.renderers = self.initializeComponent(rendererConfig) 
    def registerComponents(self, components):
        for component in components:
            cid = component['Id']
            if cid == None: 
                raise Exception('Components must have Ids!')
            self.componentDict[cid] = component
    def initializeComponent(self, config):
        components = []
        if config != None:
            for configItem in config.getchildren():
                [module,className] = configItem.find('Class').text.split('.')
                exec('from ' + module+'.'+className + ' import *')
                args = Util.generateArgDict(configItem.find('Args'))
                args['parentScope'] = self #TODO: we shouldn't give away scope
                #like this, find another way.
                components.append(eval(className+'(args)')) #TODO: doesn't error
                #right
        return components
    def alive(self):
        return True
    def mainLoop(self):
        #self.screen.allOn()
        lastLoopTime = Util.time()
        refreshInterval = 30
        while 1:
            loopStart = Util.time()
            responses = self.evaluateBehaviors() #inputs are all queued when they
            #happen, so we only need to run the behaviors
            [self.screen.respond(response) for response in responses if
                    response != []]
            self.screen.timeStep()
            [r.render(self.screen) for r in self.renderers]
            loopElapsed = Util.time()-loopStart
            sleepTime = max(0,refreshInterval-loopElapsed)
            if sleepTime > 0:
                time.sleep(sleepTime/1000)
    #evaluates all the behaviors (including inter-dependencies) and returns a
    #list of responses to go to the screen.
    def evaluateBehaviors(self):
        responses = {}
        responses['Screen'] = [] #responses to the screen
        for behavior in self.behaviors:
            responses[behavior['Id']] = behavior.timeStep()
            if behavior['RenderToScreen'] == True: #TODO: this uses extra space,
            #we can use less in the future if needbe.
                responses['Screen'] += responses[behavior['Id']]
        return responses['Screen']

    def initializeBehaviors(self, behaviorConfig):
        self.behaviors = self.initializeComponent(behaviorConfig)
        for behavior in self.behaviors:
            self.addBehavior(behavior)
    #TODO: we probably don't need this anymore :(
    def topologicalBehaviorSort(self):
        return Util.topologicalSort(self.behaviorDependencies)
    #Does work needed to add a behavior: currently -- maps behavior inputs into
    #the input behavior registry.
    def addBehavior(self, behavior):
        for inputId in behavior.argDict['Inputs']:
            if inputId in self.inputBehaviorRegistry: #it could be a behavior
                self.inputBehaviorRegistry[inputId].append(behavior['Id'])
    def processResponse(self,inputDict, responseDict):
        inputId = inputDict['Id']
        boundBehaviorIds = self.inputBehaviorRegistry[inputId]
        [self.componentDict[b].addInput(responseDict) for b in boundBehaviorIds]

def main(argv):
    print argv
    if len(argv) == 1:
        l = LightInstallation('LightInstallationConfig.xml')
    else:
        l = LightInstallation(argv[1])
if __name__ == "__main__":
    main(sys.argv)

