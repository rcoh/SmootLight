from operationscore.Behavior import *
class GenerateModulate(Behavior):
    def behaviorInit(self):
        self.stepIndex = 0
    def processResponse(self, sensors, recurs):
        """If a member of sensors is less than <ThresholdDist> away from 
        a member of recurs, the XStep of recurs is modulated accordingly an
        its lifetime returns to <Lifetime>
        Otherwise, a new recurrence is created.
        <IntersectionTime> -- the time it takes a response to merge back to 
        The LifeTime of all members of the recurrences are decremented.

        The object is moved by XStep"""
        self.stepIndex += 1
        output = []
        #first, just make a new recurs
        outRecurs = []
        numObjs = len(recurs)
        for r in recurs:#TODO: could replace with a Map
            newR = dict(r) 
            if(abs(newR['LastObs'] - newR['Location'][0]) < self['MaxDist']):
                outRecurs.append(newR)


        for newInput in sensors:
            #print 'new input'
            if newInput['Velocity'] != 0:
                mergeCandidate = self.mergeable(newInput, outRecurs)
                if(mergeCandidate != None):
                    self.modulateResponse(mergeCandidate, newInput)
                    #print 'merged'
                else:
                    #nprint 'initialized'
                    if len(recurs) < 20:
                        newResponse = dict(newInput)
                        newResponse['LastObs'] = newResponse['Location'][0]
                        newResponse['XVel'] = newInput['Velocity']
                        newResponse['TDMAId'] = numObjs
                        numObjs += 1
                        outRecurs.append(newResponse)
        strippedOutput = []
        for i,r in enumerate(recurs):
            if  i % 5 == self.stepIndex % 5:
                strippedOutput.append(r)
        if len(strippedOutput) > 0:
            #print 'stripedOut', len(strippedOutput)
            pass
        elif len(recurs) > 0:
            pass
            #import pdb; pdb.set_trace()
        if len(strippedOutput) > 10:
            #strippedOutput = strippedOutput[0:10]
            pass
        return (strippedOutput, outRecurs)
    def mergeable(self, newInput, activeResponses):
        if not activeResponses:
            return None
        searchLoc = newInput['Location'][0]
        bestRespLoc = None
        bestResp = None
        for resp in activeResponses:
            respLoc = resp['Location'][0]
            if bestRespLoc == None or abs(searchLoc - respLoc) < abs(searchLoc - bestRespLoc):
                bestRespLoc = respLoc
                bestResp = resp
        if abs(searchLoc - bestRespLoc) > self['ThresholdDist']:
            return None
        return bestResp

    def modulateResponse(self, mergeCandidate, newInput):
        diff = newInput['Location'][0] - mergeCandidate['Location'][0]
        #print 'loc', mergeCandidate['Location'][0]
        #print 'deltaloc:',diff
        #print 'vel1:', mergeCandidate['XVel']
        #positive if the newInput is ahead of the propsed merge candidate
        mergeCandidate['XVel'] = (diff+newInput['Velocity']*self['IntersectionTime']) /\
            self['IntersectionTime'] 
        #print 'vel2:', mergeCandidate['XVel']
#        mergeCandidate['XVel'] = newInput['Velocity']
        mergeCandidate['LastObs'] = mergeCandidate['Location'][0] 
