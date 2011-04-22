from operationscore.Behavior import *
import util.Geo as Geo

class PedTrack(Behavior):

    def processResponse(self, sensor, recurs):
        #Initialize dictionary. Keys: sensor_ids, Values: indicator of ped presence
        try:
            self.peds
        except:
            self.peds = {}
        print self.peds
        ret = []
        #Decrease all presence levels to a minimum of 0
        for v in self.peds.keys():
            self.peds[v] = max(0, self.peds[v] - 1)
        for sensory in sensor:
            opsensory = dict(sensory)
            if "SensorId" in opsensory:
                if "detected" not in opsensory:
                    opsensory["detected"] = True
                    sid = opsensory["SensorId"]
                    self.peds[sid] = 10
            ret.append(opsensory)

        return (ret, []) 

