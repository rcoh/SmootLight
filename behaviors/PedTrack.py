from operationscore.Behavior import *
import util.Geo as Geo

class PedTrack(Behavior):
    def processResponse(self, sensor, recurs):
        ret = []
        if self['MaxIntensity'] != None:
            maxIntensity = self['MaxIntensity']
        else:
            maxIntensity = 10
        if recurs:
            outputDict, colorDict = recurs
        else:
            outputDict = {}
            colorDict = {}
        dimKeys = []
        for key in outputDict:
            outputDict[key] -= .1
            if outputDict[key] < 0:
                dimKeys.append(key)
        for key in dimKeys:
            del outputDict[key]
        for inp in sensor:
            if inp['Location'] in outputDict:
                outputDict[inp['Location']] += 1
            else:
                outputDict[inp['Location']] = 1
        if sensor or recurs:
            if not 'Color' in colorDict:
                colorDict['Color'] = sensor[0]['Color'] 
            directOut = {'Location':outputDict, 'Color': colorDict['Color']}
            return ([directOut], [outputDict, colorDict])
        else:
            return ([],[])
