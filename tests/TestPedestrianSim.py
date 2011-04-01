import unittest
from inputs.PedestrianSimulator import *
class TestPedestrianSim(unittest.TestCase):
    def test_init(self):
        arg1 = dict(parentScope=self, MaxX=400,Velocity=40, NumSensors=40, SensorSpacing=48, NumPeds=20)
        pedSim = PedestrianSimulator(arg1)
        assert len(pedSim.sensors)==40
        assert len(pedSim.peds)==20
