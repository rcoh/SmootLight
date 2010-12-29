from xml.etree.ElementTree import ElementTree
from pixelcore.Screen import * 
from pixelcore.PixelStrip import *
import pdb, sys, time, thread
from pygame.locals import *
import util.TimeOps as clock
import util.Config as configGetter 
import util.ComponentRegistry as compReg
from logger import main_log
#Python class to instantiate and drive a Screen through different patterns,
#and effects.
class LightInstallation:
    def __init__(self, configFileName):
        main_log.info("System Initialization began based on: " + str(configFileName))
        self.timer = clock.Stopwatch()
        self.timer.start()
        self.inputs = {} #dict of inputs and their bound behaviors, keyed by InputId
        self.behaviors = {}
        self.lock = thread.allocate_lock()
        self.behaviorOutputs = {} #key: [list of output destinations]
        self.behaviorInputs = {}
        self.componentDict = {}
        self.inputBehaviorRegistry = {} #inputid -> behaviors listening to that
        #input
        self.screen = Screen()
        compReg.initRegistry()
        compReg.registerComponent(self.screen, 'Screen') #TODO: move to constants file
        config = configGetter.loadConfigFile(configFileName)
        #read configs from xml
        rendererConfig = config.find('RendererConfiguration')
        pixelConfig = config.find('PixelConfiguration')
        inputConfig = config.find('InputConfiguration')
        behaviorConfig = config.find('BehaviorConfiguration')
        mapperConfig = config.find('PixelMapperConfiguration')

        installationConfig = config.find('InstallationConfiguration')
        #inits
        self.initializeScreen(pixelConfig)
        self.initializeRenderers(rendererConfig)
        self.initializeInputs(inputConfig)
        self.initializeBehaviors(behaviorConfig)
        self.initializeMapper(mapperConfig)
        main_log.info('All components initialized')
        #registration in dict
        self.registerComponents(self.renderers)
        self.registerComponents(self.inputs)
        self.registerComponents(self.behaviors)
        self.registerComponents(self.mappers)
        self.configureInstallation(installationConfig)
        #Done initializing.  Lets start this thing!
        self.timer.stop()
        #main_log.info('Initialization done.  Time: ', self.timer.elapsed(), 'ms')
        self.mainLoop()
    def configureInstallation(self, installationConfig):
        defaults = configGetter.generateArgDict(installationConfig.find('Defaults'))
        for defaultSelection in defaults:
            componentToMap = compReg.getComponent(defaults[defaultSelection])
            compReg.registerComponent(compReg.getComponent(defaults[defaultSelection]),\
                'Default'+defaultSelection)
            main_log.debug('Default Set: ' + defaultSelection + 'set to ' +\
                defaults[defaultSelection])

    def initializeMapper(self, mapperConfig):
        self.mappers = self.initializeComponent(mapperConfig) 
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
            if cid == None:  #TODO: determine if componenent is critical, and if so, die
                main_log.error('Components must be registered with Ids.  Component not registered')
            else:
                compReg.registerComponent(component)
                main_log.debug(cid + ' registered')
    def initializeComponent(self, config):
        components = []
        if config != None:
            config = configGetter.resolveConfigInheritance(config)
            for configItem in config.getchildren():
                configItem = configGetter.resolveConfigInheritance(configItem) #resolve
                #inheritences.  TODO: migrate to a recursive inheritence resolver that gets run on
                #file-parse
                try:
                    [module,className] = configItem.find('Class').text.split('.')
                except:
                    main_log.error('Module must have Class element')
                    main_log.warn('Module without class element.  Module not initialized')
                    continue
                try:
                    exec('from ' + module+'.'+className + ' import *')
                    main_log.debug(module +'.' +className + 'imported')
                except:
                    main_log.error('Error importing ' + module+'.'+'.className.  Component not\
                    initialized.')
                    continue #TODO: verify functions as expected
                args = configGetter.generateArgDict(configItem.find('Args'))
                args['parentScope'] = self #TODO: we shouldn't give away scope
                #like this, find another way.
                try:
                    components.append(eval(className+'(args)')) #TODO: doesn't error
                    main_log.debug(className + 'initialized with args ' + str(args))
                #right
                except Exception as inst:
                    main_log.error('Failure while initializing ' + className + ' with ' + str(args))
                    #main_log.error(inst) TODO: exception logging
                
        return components
    def alive(self):
        return True
    def mainLoop(self):
        #self.screen.allOn()
        lastLoopTime = clock.time()
        refreshInterval = 30
        runCount = 10000
        while runCount > 0:
            runCount -= 1
            loopStart = clock.time()
            responses = self.evaluateBehaviors() #inputs are all queued when they
            #happen, so we only need to run the behaviors
            self.timer.start()
            [self.screen.respond(response) for response in responses if
                    response != []]
            self.screen.timeStep()
            [r.render(self.screen) for r in self.renderers]
            loopElapsed = clock.time()-loopStart
            sleepTime = max(0,refreshInterval-loopElapsed)
            self.timer.stop()
            #print self.timer.elapsed()
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
    #Does work needed to add a behavior: currently -- maps behavior inputs into
    #the input behavior registry.
    def addBehavior(self, behavior):
        for inputId in behavior.argDict['Inputs']:
            if inputId in self.inputBehaviorRegistry: #it could be a behavior
                self.inputBehaviorRegistry[inputId].append(behavior['Id'])
    def processResponse(self,inputDict, responseDict):
        inputId = inputDict['Id']
        boundBehaviorIds = self.inputBehaviorRegistry[inputId]
        #TODO: fix this, it crashes because inputs get run before beahviors exist 
        try:
            [compReg.getComponent(b).addInput(responseDict) for b in boundBehaviorIds]
        except:
            pass
            #print 'Behaviors not initialized yet.  WAIT!' 
def main(argv):
    if len(argv) == 1:
        l = LightInstallation('LightInstallationConfig.xml')
    else:
        l = LightInstallation(argv[1])
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        main_log.info('Terminated by keyboard.')
