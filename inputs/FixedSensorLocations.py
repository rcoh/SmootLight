from operationscore.Input import *

class FixedSensorLocations(Input):
    """
    FixedSensorLocation takes a descriptions of the sensor network and outputs the locations of the sensors
    """
    def inputInit(self):
        self.sensorLocs = []
        for i in range(1, self['SensorNumber']+1):
            r = {}
            r['Location'] = (i * self['SensorSpacing'], self['Y'])
            r['Color'] = (255, 255, 255)
            self.sensorLocs.append(r)

    def sensingLoop(self):
        self.respond(self.sensorLocs)
