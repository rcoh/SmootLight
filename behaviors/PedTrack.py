from operationscore.Behavior import *
import util.Geo as Geo

class PedTrack(Behavior):

    def processResponse(self, sensor, recurs):
        ret = []

        if self['MaxIntensity'] != None:
            maxIntensity = self['MaxIntensity']
        else:
            maxIntensity = 10
        outputDict = {} 
        for sensory in sensor:
            opsensory = dict(sensory)
            if "SensorId" in opsensory:
                if "detected" not in opsensory:
                    opsensory["detected"] = True
                    opsensory["Location"] = {opsensory["Location"]:maxIntensity}
                else:
                    opsensory["Location"] = {opsensory["Location"].keys()[0]:max(opsensory["Location"].values()[0] - 1, 0)}
            ret.append(opsensory)
        return (ret, [])
