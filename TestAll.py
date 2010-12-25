import unittest
from unittest import TestLoader
import tests.TestConfigLoaders 
testSuite = TestLoader().loadTestsFromModule(tests.TestConfigLoaders)
unittest.TextTestRunner(verbosity=2).run(testSuite)
