#!/usr/bin/python

from xml.etree.ElementTree import ElementTree
from pixelcore.Screen import * 
import pdb, sys, time, thread
import util.TimeOps as clock
import util.Config as configGetter 
import util.ComponentRegistry as compReg
import util.BehaviorQuerySystem as bqs
from logger import main_log
#Python class to instantiate and drive a Screen through different patterns,
#and effects.
class LightInstallation(object):
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
        self.dieNow = False
        #input
        self.screen = Screen()
        compReg.initRegistry()
        compReg.registerComponent(self.screen, 'Screen') #TODO: move to constants file
       
        bqs.initBQS()   #initialize the behavior query system
        #read configs from xml
        config = configGetter.loadConfigFile(configFileName)
        
        rendererConfig = config.find('RendererConfiguration')
        self.initializeRenderers(rendererConfig)
        
        pixelConfig = config.find('PixelConfiguration')
        self.initializeScreen(pixelConfig)
        
        inputConfig = config.find('InputConfiguration')
        self.initializeInputs(inputConfig)
        
        behaviorConfig = config.find('BehaviorConfiguration')
        self.initializeBehaviors(behaviorConfig)
        
        mapperConfig = config.find('PixelMapperConfiguration')
        self.initializeMapper(mapperConfig)

        #inits
        main_log.info('All components initialized')
        #
        self.registerAllComponents()
        
        installationConfig = config.find('InstallationConfiguration')
        self.configureInstallation(installationConfig)
        #Done initializing.  Lets start this thing!
        self.timer.stop()
        #main_log.info('Initialization done.  Time: ', self.timer.elapsed(), 'ms')
        self.mainLoop()
    
    def registerAllComponents(self):
        #registration in dict
        self.registerComponents(self.renderers)
        self.registerComponents(self.inputs)
        self.registerComponents(self.behaviors)
        self.registerComponents(self.mappers)
        
    
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
        self.screen.initStrips(pixelAssemblers)
    
    def initializeInputs(self, inputConfig):
        inputs = self.initializeComponent(inputConfig)
        self.inputs = inputs
        for inputClass in inputs:
            self.inputBehaviorRegistry[inputClass['Id']] = [] #Bound behaviors will be added to this
            inputClass.start()
            #list
            
    def initializeRenderers(self, rendererConfig):
        self.renderers = self.initializeComponent(rendererConfig) 
        
    def registerComponents(self, components):
        for component in components:
            cid = compReg.registerComponent(component)
            if cid == None:
                raise Exception('Null component Id.  ComponentRegistry not fuctioning as expected.')
            main_log.info(cid + ' registered')
    def initializeComponent(self, config):
        components = []
        if config != None:
            for configItem in config.getchildren():
                try:
                    [module,className] = configItem.find('Class').text.split('.')
                except:
                    main_log.error('Module must have Class element')
                    continue
                try:
                    exec('from ' + module+'.'+className + ' import *')
                    main_log.debug(module +'.' +className + 'imported')
                except Exception as inst:
                    main_log.error('Error importing ' + module+'.'+className+ '.  Component not\
                    initialized.')
                    main_log.error(str(inst)) 
                    continue 
                args = configGetter.pullArgsFromItem(configItem)
                args['parentScope'] = self 
                try:
                    new_component = eval(className+'(args)')
                    new_component.addDieListener(self)
                    components.append(new_component) 
                    main_log.info(className + 'initialized with args ' + str(args))
                except Exception as inst:
                    main_log.error('Failure while initializing ' + className + ' with ' + str(args))
                    main_log.error(str(inst)) 
                
        return components
        
    def alive(self):
        return True
    
    def mainLoop(self):
        lastLoopTime = clock.time()
        refreshInterval = 30 
        while not self.dieNow: #dieNow is set if one of its constituents sends a die request.
            loopStart = clock.time()
            responses = self.evaluateBehaviors() 
            self.timer.start()
            [self.screen.respond(response) for response in responses if
                    response != []]
            self.screen.timeStep(loopStart)
            [r.render(self.screen, loopStart) for r in self.renderers]
            loopElapsed = clock.time()-loopStart
            #if loopElapsed > 100:
            #print 'loop elapsed: ', loopElapsed 
            sleepTime = max(0,refreshInterval-loopElapsed)
            main_log.debug('Loop complete in {0} ms.  Sleeping for {1} ms.'.format(loopElapsed, sleepTime))
            self.timer.stop()
            if sleepTime > 0:
                time.sleep(sleepTime/1000)
                
    def evaluateBehaviors(self):
        """Evaluates all the behaviors (including inter-dependencies) and returns a list of responses to
        go to the screen"""
        responses = {}
        responses['Screen'] = [] #responses to the screen
        for behavior in self.behaviors:
            if behavior['RenderToScreen'] == True: 
                responses[behavior['Id']] = behavior.timeStep()
                responses['Screen'] += responses[behavior['Id']]
        return responses['Screen']

    def initializeBehaviors(self, behaviorConfig):
        self.behaviors = self.initializeComponent(behaviorConfig)
        for behavior in self.behaviors:
            self.addBehavior(behavior)
            bqs.addBehavior(behavior)
            
    def addBehavior(self, behavior):
        """Does work needed to add a behavior: currently -- maps behavior inputs into the input behavior
        registry"""
        for inputId in behavior.argDict['Inputs']:
            if inputId in self.inputBehaviorRegistry: #it could be a behavior
                self.inputBehaviorRegistry[inputId].append(behavior['Id'])
                
    def processResponse(self,inputDict, responseDict):
        inputId = inputDict['Id']
        try:
            boundBehaviorIds = self.inputBehaviorRegistry[inputId]
        except KeyError:
            print "missing input"
            return
            
        if not isinstance(responseDict, list):
            responseDict = [responseDict]
        try:
            for r in responseDict:
                for b in boundBehaviorIds:
                    c = compReg.getComponent(b)
                    # Only accept inputs to rendering behaviors, since they can pile up
                    # MAY CAUSE DISCONTINUITY if behavior continuity is dependent on input continuity
                    if c['RenderToScreen']:
                        c.addInput(r)
        except:
            pass
            #Behavior run before loading.  Not a big deal.
            
    def handleDie(self, caller):
        self.dieNow = True
            
def main(argv):
    if len(argv) == 1:
        l = LightInstallation('config/6thFloor.xml')
    else:
        l = LightInstallation(argv[1])
        
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        main_log.info('Terminated by keyboard.')
