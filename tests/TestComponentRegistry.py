import unittest
import util.ComponentRegistry as compReg
from operationscore.SmootCoreObject import SmootCoreObject 
class TestComponentRegistry(unittest.TestCase):
    def setUp(self):
        compReg.initRegistry()

    def tearDown(self):
        compReg.clearRegistry()
    
    def test_register_component_id_specified(self):
        comp = SmootCoreObject({'Id': 'obj1'})
        compReg.registerComponent(comp)
        newcomp = compReg.getComponent('obj1')
        assert comp == newcomp
    
    def test_register_new_id(self):
        comp = SmootCoreObject({})
        cid =compReg.registerComponent(comp)
        newcomp = compReg.getComponent(cid)
        assert comp == newcomp
            
