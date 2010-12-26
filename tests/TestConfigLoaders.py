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

if __name__ == '__main__':
    unittest.main()
