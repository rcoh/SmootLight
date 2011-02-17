import unittest
import util.ComponentRegistry as compReg

from behaviors.SwitchBehavior import SwitchBehavior
from behaviors.EchoBehavior import EchoBehavior
from behaviors.DebugBehavior import DebugBehavior

class TestSwitchBehavior(unittest.TestCase):
    def setUp(self):
        compReg.initRegistry()

        # add a test registry
        self.behavior1 = EchoBehavior({'Id': 'behavior1'})
        self.behavior2 = DebugBehavior({'Id': 'behavior2'})
        compReg.registerComponent(self.behavior1)
        compReg.registerComponent(self.behavior2)

        self.switchBehavior = SwitchBehavior({'Id': 'switch', 'PrefixToBehavior': '{"@": "behavior1", "#": "behavior2"}', 'DefaultBehavior': 'behavior1'})
        compReg.registerComponent(self.switchBehavior)

    def tearDown(self):
        pass

    def test_switch_to_behavior1(self):
        inputs = [{'Data': '@something', 'Location': 'someloc'}]
        returned = self.switchBehavior.processResponse(inputs, [])
        assert returned[0][0]['Location'] == 'someloc'

    def test_switch_to_behavior2(self):
        inputs = [{'Data': '#something'}]
        returned = self.switchBehavior.processResponse(inputs, [])
        assert returned[0] == []

    def test_default_behavior(self):
        inputs = [{'Data': 'something', 'Location': 'someloc'}]
        returned = self.switchBehavior.processResponse(inputs, [])
        assert returned[0][0]['Location'] == 'someloc'
    

if __name__ == '__main__':
    unittest.main()
