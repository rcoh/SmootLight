from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json
from behaviors import LocationBasedEvent, BehaviorChain
from logger import main_log
class SystemConfigMutator(Behavior):
    """SystemConfigMutator is a behavior which performs CRUD operations on the configuration of 
    the system according to its input.  It requires the following parameters of its input dicts:
        'OperationType' -- the type of modification to perform.  Possible values:
            'Create' -- Create a new componenent -- NOT SUPPORTED
            'Read'   -- Gets current configuration data as JSON
            'Update' -- Assign a parameter of a currently existing component
            'Destroy' -- Removes a componenent -- NOT SUPPORTED
        'Callback' -- a function which will be called with the results of the mutation.

        If you are performing a 'Create' you must define the following parameters:
            'Class' -- the fully qualified python class defining the behavior.  EG:
                behaviors.SystemConfigMutator
            'Args' -- The args dict for the class.
            
        If you are performing a 'Read' you must define the following parameters:
            'Callback' -- a function to which the response will be sent
            'OperationDetail' -- what to retrieve: 'Objects' (all objects), 'Behaviors', 'Inputs'(not supported)
            'OperationArg' -- optional, if specified, will only return details about the named object
            
        If you are performing an 'Update' you must define the following parameters:
            'ComponentId' -- The Id of the component to modify
            'ParamName' -- The name of the parameter to modify
            'Value' -- The value to set on the chosen component and parameter
    
        If you are performing a 'Destroy' you must define the following parameters:
            'ComponentId' -- The Id of the component to remove.  
            WARNING: Make sure that the component you are removing is not referenced by other
            components if you don't want to bork the system.

        'Callback' should by a function pointer that accepts a 
        tuple of (bool, message) where bool indicates whether or not the
        mutatation suceeded. The message provides greater clarification."""
    def doRead(self,packet):
        cb = packet['Callback']
        detail = packet['OperationDetail']
        
        if packet.has_key('OperationArg') and packet['OperationArg'] != None:
            arg = packet['OperationArg']
            if compReg.Registry.has_key(arg):
                reply = str(compReg.getComponent(arg).argDict)
            else:
                reply = "null"
        else:
            if detail == 'Renderables':
                reply = [[x[0],x[1].argDict['RenderToScreen']]for x in compReg.Registry.items() if \
                    issubclass(type(x[1]),Behavior) and x[1].argDict.has_key('RenderToScreen') and x[0]!='mutation']
            elif detail == 'Objects':
                reply = [[x] for x in compReg.Registry.keys()]
            elif detail == 'Behaviors':
                reply = [[x[0]] for x in compReg.Registry.items() if issubclass(type(x[1]),Behavior)]
        cb(json.dumps(reply))
    
    def isValidValue(obj,name,val):
        if hasattr(obj, '__call__'):
            valid = obj(val)
        elif type(obj) is type:
            valid = (type(val) is obj)
        elif type(obj) is list:
            valid = (val in obj)
        else:
            main_log.debug("invalid validator, need lambda,list,or type: "+str(obj))
            
        
            
    def processResponse(self, data, recurs):
        for packet in data:
            message = ""
            try:
                if not 'OperationType' in packet:
                    packet['OperationType'] = 'Update'
                
                if packet['OperationType'] == 'Create':
                    raise Exception('Create is not supported')
                    compFactory.create(packet['Class'], packet['Args'])
                elif packet['OperationType'] == 'Read':                    
                    self.doRead(packet)
                elif packet['OperationType'] == 'Update':
                    cid = packet['ComponentId']
                    paramName = packet['ParamName']
                    newParamValue = packet['Value'] 
                    currentObject=compReg.getComponent(cid)
                    if paramName == 'RenderToScreen':
                        if newParamValue == True or type(newParamValue) is str and newParamValue[0].lower=='t':
                            newParamValue = True
                        elif newParamValue == False or type(newParamValue) is str and newParamValue[0].lower=='f':
                            newParamValue = False
                        else:
                            newParamValue = None
                        if newParamValue is not None:
                            currentObject['RenderToScreen'] = newParamValue
                    elif currentObject.has_key('Mutable') and currentObject['Mutable'].has_key(paramName):
                        if is_valid(currentObject['Mutable'][paramName], newParamValue):
                            currentObject[paramName] = newParamValue
                    else:
                        raise Exception('Non-mutable parameter specified.') # don't allow anything else for security purposes
                    #TODO: consider adding lambda evaluation capabilities
                elif packet['OperationType'] == 'Destroy':
                    raise Exception('Destroy not supported')
                    compReg.removeComponent(packet['ComponentId'])
            except Exception, e:
                print str(e)
                import pdb; pdb.set_trace()
        return ([],[])

