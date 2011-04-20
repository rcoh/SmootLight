from operationscore.Behavior import *
class GenerateModulate(Behavior):
    def processResponse(self, sensors, recurs):
        """If a member of sensors is less than <ThresholdDist> away from 
        a member of recurs, the XStep of recurs is modulated accordingly an
        its lifetime returns to <LifeTime>
        Otherwise, a new recurrence is created.

        The LifeTime of all members of the recurrences are decremented.

        The object is moved by XStep"""
        output = []
        #first, just make a new recurs
        outRecurs = []
        for r in recurs:#TODO: could replace with a Map
            outRecurs.append(dict(r))


        for newInput in sensors:
            mergeCandidate = self.mergeable(newInput, outRecurs)
            if(mergeCandidate != None):
                self.modulateResponse(mergeCandidate, newInput)
            else:
                newResponse = dict(newInput)
                if newInput['Velocity'] != 0:
                    newResponse['XVel'] = newInput['Velocity']
                    outRecurs.append(newResponse)

        return (recurs, outRecurs)
    def mergeable(self, newInput, activeResponses):
        searchLoc = newInput['Location'][0]
        bestRespLoc = None
        bestResp = None
        for resp in activeResponses:
            respLoc = resp['Location'][0]
            if bestRespLoc == None or abs(searchLoc - respLoc) < abs(searchLoc - bestResp):
                bestRespLoc = respLoc
                bestResp = resp
        if abs(searchLoc - bestResp) > self['ThresholDist']):
            return None
        return bestResp

    def modulateResponse(mergeCandidate, newInput):
        diff = newInput['Location'][0] - mergeCandidate['Location'][0]
        #positive if the newInput is ahead of the propsed merge candidate
        mergeCandidate['XVel'] = (diff+newInput['Velocity']*self['IntersectionTime']) /\
            self['IntersectionTime'] 
