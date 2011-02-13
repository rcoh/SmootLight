from operationscore.Behavior import *
import math
import pdb
#Class to perform a given operation on some element of an argDict.  Designed to be used a recursive hook, but can serve sensor-based functions as well.  Specify ParamType (Sensor or Recurse), ParamName, and ParamOp, (a valid python statement with the old value represented as {val})
class ModifyParam(Behavior):
    """ModifyParam is a powerful class to perform an action on a specified key in the Argument
    Dictionary of a response.  Specify:
    <ParamType> -- Sensor or Recurse
    <ParamName> -- The name of the parameter you wish to modify
    <ParamOp> -- The modification you wish to do.  Use {val} to specify the current value of the
    parameter in question.  Special hooks for {x} and {y} also exist to access the x and y
    locations."""

    def processResponse(self, sensorInputs, recursiveInputs):
        paramType = self['ParamType']
        if paramType == None:
            paramType = 'Sensor'
        paramName = self['ParamName']
        paramOp = str(self['ParamOp'])
        if paramType == 'Sensor':
            searchSet = sensorInputs
        elif paramType == 'Recurse':
            searchSet = recursiveInputs    
        else:
            raise Exception('Unknown Param Type')
        for behaviorInput in searchSet:
            if paramName in behaviorInput: #TODO: copy -> modify instead of just
            #copying
                    paramOp = paramOp.replace('{val}', 'behaviorInput[paramName]') #convert the {val} marker to something we can execute
                    #TODO: move elsewhere
                    paramOp = paramOp.replace('{y}', "behaviorInput['Location'][1]")
                    paramOp = paramOp.replace('{x}', "behaviorInput['Location'][0]")
                    if eval(paramOp) == None:
                        import pdb; pdb.set_trace()
                    behaviorInput[paramName] = eval(paramOp)
        if paramType == 'Sensor': #return accordingly
            return (searchSet, recursiveInputs)
        if paramType == 'Recurse':
            return (sensorInputs, searchSet)

