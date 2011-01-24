import unittest
from unittest import TestLoader
import tests.TestConfigLoaders 
import tests.TestComponentRegistry
testSuite = TestLoader().loadTestsFromModule(tests.TestConfigLoaders)
unittest.TextTestRunner(verbosity=2).run(testSuite)

testSuite = TestLoader().loadTestsFromModule(tests.TestComponentRegistry)
unittest.TextTestRunner(verbosity=2).run(testSuite)
