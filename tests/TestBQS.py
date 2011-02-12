import unittest
import util.BehaviorQuerySystem as bqs
from behaviors.ColorChangerBehavior import *
class TestBQS(unittest.TestCase):
    def setUp(self):
        bqs.initBQS()
        b = ColorChangerBehavior({'Id': 'color','ColorList':[(255,0,0)]})
        bqs.addBehavior(b)
        b.addInput({'Location':(5,5)})
        b.timeStep()
    def tearDown(self):
        bqs.initBQS()

    def test_color_predicate(self):
        validQuery = lambda args:args['Color']==(255,0,0)
        invalidQuery = lambda args:args['Color']==(254,0,0)
        assert bqs.query(validQuery) == [{'Color':(255,0,0), 'Location':(5,5)}]
        assert bqs.query(invalidQuery) == []
