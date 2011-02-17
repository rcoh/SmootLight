import unittest
from unittest import TestLoader
import tests

testSuite = TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner(verbosity=2).run(testSuite)

