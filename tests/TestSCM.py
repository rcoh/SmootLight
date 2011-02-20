import unittest
import util.ComponentRegistry as compReg
from behaviors.ColorChangerBehavior import *
from inputs.ContinuousCenterInput import *
from behaviors.SystemConfigMutator import *
from pixelcore.Screen import *
class TestSCM(unittest.TestCase):
    def setUp(self):
        s = Screen()
        compReg.registerComponent(s, 'Screen')
        
        b = ColorChangerBehavior({'Id': 'color','ColorList':[(255,0,0)]})
        i = ContinuousCenterInput({'Id': 'center','parentScope':self,'RefreshInterval':500})
        
        compReg.registerComponent(b)
        compReg.registerComponent(i)
        

    def test_modify_components(self):
        modifier = SystemConfigMutator({'Id':'mutate'})
        params = {'Value':(0,0,255)}
        modifier.immediateProcessInput([{'OperationType':'Assign',\
                                        'ComponentId':'color','ParamName':'ColorList',\
                                        'Value':[(0,0,255)]}],[])
        
        assert compReg.getComponent('color')['ColorList'] == [(0,0,255)]
        
        modifier.immediateProcessInput([{'OperationType':'Assign',
                                         'ComponentId':'center',
                                         'ParamName':'RefreshInterval',
                                         'Value':800}],[])
        assert compReg.getComponent('center')['RefreshInterval'] == 800
