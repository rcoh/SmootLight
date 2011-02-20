import util.componentRegistry as compReg
def createComponent(className, args):
    """Creates a component.  
    className -- A fully qualified class name: Eg. behaviors.SystemConfigMutator
    args -- the args dict for the class"""
    try:
        [module,className] = className 
    except:
        main_log.error('Module must have Class element')
        raise Exception('Module must have Class element.  Component not initialized')        
    try:
        exec('from ' + module+'.'+className + ' import *')
        main_log.debug(module +'.' +className + 'imported')
    except Exception as inst:
        main_log.error('Error importing ' + module+'.'+className+ '.  Component not\
        initialized.')
        raise Exception('Error importing ' + module+'.'+className+ '.  Component not\
        initialized.')
        main_log.error(str(inst)) 
    try:
        new_component = eval(className+'(args)')
        new_component.addDieListener(self)
        main_log.info(className + 'initialized with args ' + str(args))
        return new_component
    except Exception as inst:
        main_log.error('Failure while initializing ' + className + ' with ' + str(args)+': ' +\
            str(inst))
        raise Exception('Failure while initializing ' + className + ' with ' + str(args)+': ' +\
            str(inst))

