import unittest
import util.BehaviorQuerySystem as bqs
from behaviors.ColorChangerBehavior import *
import util.Geo as geo
class TestBQS(unittest.TestCase):
    def setUp(self):
        bqs.initBQS()
        b = ColorChangerBehavior({'Id': 'color','ColorList':[(255,0,0)]})
        c = ColorChangerBehavior({'Id': 'color2', 'ColorList':[(0,0,255)]})
        bqs.addBehavior(b)
        bqs.addBehavior(c)
        b.addInput({'Location':(3,4)})
        c.addInput({'Location':(5,12)})
        b.timeStep()
        c.timeStep()

    def tearDown(self):
        bqs.initBQS()

    def test_simple_query(self):
        validQuery = lambda args:args['Color']==(255,0,0)
        invalidQuery = lambda args:args['Color']==(254,0,0)
        import pdb; pdb.set_trace()
        assert bqs.query(validQuery) == [{'Color':(255,0,0), 'Location':(3,4), 'BehaviorId':'color'}]
        assert bqs.query(invalidQuery) == []
    def test_uri_query(self):
        mydict = {'UniqueResponseIdentifier':'abc'}
        goodict = {'UniqueResponseIdentifier':'cde'}
        urichecker = bqs.getDifferentUIDLambda('abc')
        assert urichecker(mydict) == False
        assert urichecker(goodict) == True
    def test_dist_query(self):
        validDist = lambda args:geo.dist(args['Location'], (0,0)) <= 5
        invalidDist = lambda args:geo.dist(args['Location'], (0,0)) <= 2
        doubleDist = lambda args:geo.dist(args['Location'], (0,0)) <= 20

        assert bqs.query(validDist) == [{'Color':(255,0,0), 'Location':(3,4), 'BehaviorId':'color'}] 
        assert bqs.query(invalidDist) == [] 
        assert bqs.query(doubleDist) == [{'Color':(255,0,0), 'Location':(3,4), 'BehaviorId':'color'}, {'Color':(0,0,255),\
                                         'Location':(5,12), 'BehaviorId':'color'}] 
    def test_complex_queries(self):
        validQuery = lambda args:args['Color']==(255,0,0)
        doubleDist = lambda args:geo.dist(args['Location'], (0,0)) <= 20
        
        twoPartPredicate = lambda args:doubleDist(args) and validQuery(args)
        assert bqs.query(twoPartPredicate) == [{'Color':(255,0,0), 'Location':(3,4)}] 
        assert bqs.query([validQuery, doubleDist]) == [{'Color':(255,0,0), 'Location':(3,4)}] 

