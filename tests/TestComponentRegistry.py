import unittest
import util.ComponentRegistry as compReg
class TestComponentRegistry(unittest.TestCase):
    def setUp(self):
        compReg.initRegistry()
    def tearDown(self):
        compReg.clearRegistry()
    def test_register_component(self):
        comp = SmootCoreObject({'Id': obj1})
        compReg.registerComponent(comp)
            
