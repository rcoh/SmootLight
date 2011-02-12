import unittest
import util.Config as Config
import pdb
from xml.etree.ElementTree import *
import filecmp
import xml
class TestConfigLoaders(unittest.TestCase):
    def setUp(self):
        pass
 
    def tearDown(self):
        pass
    
    def test_composite(self):
        parent = ElementTree()
        overrider = ElementTree()
        
        parent.parse('tests/testdata/parent.xml')
        overrider.parse('tests/testdata/override.xml')

        result = Config.compositeXMLTrees(parent,overrider)
        result = ElementTree(result)
        result.write('tests/testdata/compositeTESTout.xml')
        assert filecmp.cmp('tests/testdata/compositeTESTout.xml','tests/testdata/compositeTRUTH.xml') 
    
    def test_inheritance(self):
        result = Config.loadConfigFile('tests/testdata/inheritanceTEST.xml')

        result.write('tests/testdata/inheritanceTESTout.xml')
        assert filecmp.cmp('tests/testdata/inheritanceTESTout.xml',\
            'tests/testdata/inheritanceTRUTH.xml')
    #Tests our fancy new XML Eval Function
    def test_eval(self):
        assert Config.attemptEval('5') == 5
        assert Config.attemptEval('{5:10, 12:15}') == {5:10, 12:15}
        singleLayerLambda = Config.attemptEval('${Val}$*5')
        assert singleLayerLambda({'Val':2}) == 10 
        doubleLayerLambda = Config.attemptEval("${Val1}$*'${Val2}$'")
        assert doubleLayerLambda({'Val1':3})({'Val2':7}) == 21

        conditional = Config.attemptEval("${Val1}$*5=='${Val2}$'")
        assert conditional({'Val1':5})({'Val2':25}) == True
        assert conditional({'Val1':5})({'Val2':26}) == False 

        onlyDouble = Config.attemptEval("'${Val1}$'*'${Val2}$'")
        assert onlyDouble({})({'Val1':3, 'Val2':7}) == 21
if __name__ == '__main__':
    unittest.main()
