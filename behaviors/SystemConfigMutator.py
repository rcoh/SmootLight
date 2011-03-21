from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import json

class SystemConfigMutator(Behavior):
    """SystemConfigMutator is a behavior which modifies the configuration of the system according to
    its input.  It requires the following parameters of its input dicts:
        'OperationType' -- the type of modification to perform.  Possible values:
            'Assign' -- Assign a parameter of a currently existing component
            'Create' -- Create a new componenent -- NOT SUPPORTED
            'Remove' -- Removes a componenent -- NOT SUPPORTED
        'Callback' -- a function which will be called with the results of the mutation.

        If you are performing an 'Assign' you must define the following parameters:
            'ComponentId' -- The Id of the component to modify
            'ParamName' -- The name of the parameter to modify
            'Value' -- The value to set on the chosen component and parameter
        
        If you are performing a 'Create' you must define the following parameters:
            'Class' -- the fully qualified python class defining the behavior.  EG:
                behaviors.SystemConfigMutator
            'Args' -- The args dict for the class.
    
        If you are performing a 'Remove' you must define the following parameters:
            'ComponentId' -- The Id of the component to remove.  
            WARNING: Make sure that the component you are removing is not referenced by other
            components if you don't want to bork the system.

        'Callback' should by a function pointer that accepts a 
        tuple of (bool, message) where bool indicates whether or not the
        mutatation suceeded. The message provides greater clarification."""
    def processResponse(self, data, recurs):
        for packet in data:
            message = ""
            try:
                if not 'OperationType' in packet:
                    packet['OperationType'] = 'Assign'
                
                if packet['OperationType'] == 'Get':
                    cb = packet['Callback']
                    detail = packet['OperationDetail']
                    
                    if packet.has_key('OperationArg') and packet['OperationArg'] != None:
                        arg = packet['OperationArg']
                        if compReg.Registry.has_key(arg):
                            reply = str(compReg.getComponent(arg))
                        else:
                            reply = "null"
                    else:
                        
                        if detail == 'Objects':
                            reply = compReg.Registry.keys()
                        elif detail == 'Behaviors':
                            reply = [x[0] for x in compReg.Registry.items() if issubclass(type(x[1]),Behavior)]
                    cb(json.dumps(reply))
                 
                elif packet['OperationType'] == 'Assign':
                    cid = packet['ComponentId']
                    paramName = packet['ParamName']
                    newParamValue = packet['Value'] 
                    #TODO: consider adding lambda evaluation capabilities
                    compReg.getComponent(cid)[paramName] = newParamValue
                elif packet['OperationType'] == 'Create':
                    raise Exception('Add is not supported')
                    compFactory.create(packet['Class'], packet['Args'])
                elif packet['OperationType'] == 'Remove':
                    raise Exception('Remove not supported')
                    compReg.removeComponent(packet['ComponentId'])
            except Exception, e:
                print str(e)
                import pdb; pdb.set_trace()
        return ([],[])

