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
            <InputMap>
                <Input1Id> #actual input id of input
                    <Id>...</Id> # behaviorId which takes the input
                    ...
                </Input1Id>
                ...
            </InputMap> # looks at the InputId of the incoming inputs, and
                        # sorts them into the appropriate behaviors.
                        # if an input does not have a behavior, it is given
                        # to all behaviors
        </Args>
    </Behavior>
    """

    def behaviorInit(self):
        self.inputMap = {}
        if 'InputMap' in self.argDict:
            for inp in self['InputMap']:
                if isinstance(self['InputMap'][inp], str):
                    self.inputMap[inp] = [self['InputMap'][inp]]
                else:
                    self.inputMap[inp] = self['InputMap'][inp]
        
    def processResponse(self, inputs, state):

        out = []
        newstate = {}
        mappedinp = {}
        allinp = []

        for behaviorId in self['BehaviorList']:

            mappedinp[behaviorId] = []

            if behaviorId in state:
                behaviorState = state[behaviorId]
            else:
                behaviorState = []

        for inp in inputs:
            inpId = inp['InputId']

            if inpId in self.inputMap:
                for beh in self.inputMap[inpId]:
                    mappedinp[beh].append(inp)
            else:
                allinp.append(inp)

        for behaviorId in self['BehaviorList']:

            behavior = compReg.getComponent(behaviorId)

            #print behaviorId, " ", str(inp), ",", str(behaviorState)
            output = behavior.immediateProcessInput(
                        mappedinp[behaviorId] + list(allinp), behaviorState)
            (behaviorOutput, behaviorState) = output
            #print "  -->", str(behaviorState), ",", str(behaviorOutput)
            
            newstate[behaviorId] = behaviorState
            out.extend(behaviorOutput)

        return (out, newstate)
