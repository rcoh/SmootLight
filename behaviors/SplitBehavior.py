from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class SplitBehavior(Behavior):
    """SplitBehavior takes a list of behaviors, runs the input on all behaviors
    listed, and then returns the concantenation of all the behavior outputs.
    Behavior list is given under tag <BehaviorList> as a list of Id's
    
    Example:
    <Behavior>
        <Class>behaviors.SplitBehavior</Class>
        <Args>
            <Id>splitbehavior</Id>
            <BehaviorList>
                <Id>behavior1Id</Id>
                <Id>behavior2Id</Id>
            </BehaviorList>
        </Args>
    </Behavior>
    """

    def behaviorInit(self):
        pass
        
    def processResponse(self, inp, state):

        out = []
        newstate = {}
        for behaviorId in self['BehaviorList']:

            behavior = compReg.getComponent(behaviorId)
            if behaviorId in state:
                behaviorState = state[behaviorId]
            else:
                behaviorState = []

            #print behaviorId, " ", str(inp), ",", str(behaviorState)
            output = behavior.immediateProcessInput(inp, behaviorState)
            (behaviorOutput, behaviorState) = output
            #print "  -->", str(behaviorState), ",", str(behaviorOutput)
            
            newstate[behaviorId] = behaviorState
            out.extend(behaviorOutput)

        return (out, newstate)
