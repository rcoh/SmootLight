import types 
"""The behavior query system is a module that allows querying behaviors based on lambda-function
predicates."""
def initBQS():
    global behaviorList, initialized
    behaviorList = [] 
    initialized = True

def addBehavior(behavior):
    """Add a behavior to the behavior registry."""
    behaviorList.append(behavior)

def query(predicateList):
    """BehaviorQuerySystem.query takes a list of predicates (functions with signature:
        (behavior,output)), and
    optionally a behavior to be compared to."""
    #want to do queries wrt: behavior itself, the behavior packet, the querying behavior
    if isinstance(predicateList, types.FunctionType):
        predicateList = [predicateList]
    elif not isinstance(predicateList, list):
        raise Exception('Predicate list must be a function or list of functions')
    global behaviorList, initialized
    ret = [] 
    if not initialized:
        initBQS()
    
    for behavior in behaviorList: #Consider every behavior
        lastOutput = behavior.getLastOutput()
        for output in lastOutput: #Look at every element it has output
            validOutput = True
            for pred in predicateList: #Evaluate every predicate.  A predicate is a lambda function that
            #takes a dict and returns a bool.
                if not pred(output):
                    validOutput = False
                    break
            if validOutput:
                ret.append(output)
    return ret 

def getDistLambda(loc, maxDist):
    """Returns a lambda function that checks if for behaviors within maxDist of loc.  Can be passed
    in as an arg to query."""
    return lambda args:geo.dist(args['Location'], loc) <= maxDist

def getBehaviorsNear(loc, maxdist):
    """A premade method to do the common task of finding behavior near a location."""
    return query(getDistLambda(loc, maxDist))
