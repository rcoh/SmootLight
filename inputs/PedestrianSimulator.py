from operationscore.Input import *
from inputs.MotionSensorSimulator import *
import random
import thread
class PedestrianSimulator(Input):
    """Simulates pedestrians inputing to simulated motion sensors.
    Params:
        MaxX
        Velocity
        NumSensors
        SensorSpacing
        NumPeds
    """
    def inputInit(self):
        self.peds = []
        self.responses = []
        self.lock = thread.allocate_lock() #TODO: refactor to LockingInput
        self.sensors = []
        self.initPedestrians(self['NumPeds'], self['Velocity'], self['MaxX'])
        self.initSensors()
        #TODO: homogenize 
    def initSensors(self):
        x = 0
        for i in range(self['NumSensors']):
            sensor = MotionSensorSimulator({'Id':str(i), 'parentScope':self,'DataHook':self,
                                            'RefreshInterval':500, 'Location':x})
            x += self['SensorSpacing']
            self.sensors.append(sensor)
    def initPedestrians(self,numPeds, vel, maxX):
        for i in xrange(numPeds):
            if random.random() > .5:
                vel *= -1
            self.peds.append({'Loc':random.randint(0, maxX), 'Vel':vel})
    def getLocs(self):
        return [ped['Loc'] for ped in self.peds]
    def addPedestrian(self, loc, vel):
        self.peds.append({'Loc':loc,'Vel':vel})
    def evaluateSensors(self):
        for s in self.sensors:
            s.sensingLoop()
    def sensingLoop(self):
        self.evaluateSensors()
        self.movePedestrians(self['RefreshInterval'])
        if self.responses:
            self.respond(self.responses)
        self.responses = []
    def processResponse(self, sensorInput):
        """Queue up response""" 
        self.responses.append(sensorInput)
    def movePedestrians(self, dt):
        for ped in self.peds:
            ped['Loc'] += ped['Vel'] * dt/1000
