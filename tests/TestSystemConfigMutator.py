import unittest
import util.ComponentRegistry as compReg
from behaviors.ColorChangerBehavior import *
from inputs.ContinuousCenterInput import *
from behaviors.SystemConfigMutator import *
class TestSCM(unittest.TestCase):
    def setUp(self):
        b = ColorChangerBehavior({'Id': 'color','ColorList':[(255,0,0)]})
        i = ContinuousCenterInput({'Id': 'center','parentScope':self,'RefreshInterval':500})
        compReg.registerComponent(b)
        compReg.registerComponent(i)

    def test_modify_components(self):
        modifier = SystemConfigMutator({'Id':'mutate'})
        modifier.immediateProcessInput({'OperationType':'Update',\
                                        'ComponentId':'color','ParamName':'ColorList',
                                        'Value':[(0,0,255)]})
        
        assert compReg.getComponent('color')['ColorList'] == [(0,0,255)]
        
        modifier.immediatedProcessInput({'OperationType':'Update',
                                         'ComponentId':'center',
                                         'ParamName':'RefreshInterva',
                                         'Value':800})
        
        assert compReg.getComponent('center')['RefreshInterval'] == 800
